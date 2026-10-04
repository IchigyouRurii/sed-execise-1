import io
import json
import os
import unittest
from unittest.mock import patch

with patch.dict(os.environ, {'DATABASE_URL': ''}):
    from src.main import app


class TranslateRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_translates_title_and_content_without_saving(self):
        notes_before = self.client.get('/api/notes').get_json()
        translated = {'title': '准备烧烤', 'content': '物品：\n- 猪肉\n- 鸡肉'}
        provider_response = {
            'choices': [{'message': {'content': json.dumps(translated, ensure_ascii=False)}}]
        }
        provider_stream = io.BytesIO(json.dumps(provider_response).encode('utf-8'))

        with patch.dict(os.environ, {
            'OPENROUTER_API_KEY': 'test-key',
            'OPENROUTER_MODEL': 'qwen/qwen3.8-27b:free',
        }):
            with patch('src.routes.translate.urlopen', return_value=provider_stream) as urlopen:
                response = self.client.post('/api/translate', json={
                    'title': 'Prepare BBQ',
                    'content': 'Items:\n- Pork\n- Chicken',
                    'target_language': 'zh',
                })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), translated)
        self.assertEqual(urlopen.call_count, 1)
        upstream_request = urlopen.call_args.args[0]
        self.assertEqual(upstream_request.full_url, 'https://openrouter.ai/api/v1/chat/completions')
        payload = json.loads(upstream_request.data)
        self.assertEqual(payload['model'], 'qwen/qwen3.8-27b:free')
        self.assertEqual(payload['messages'][1]['content'], json.dumps({
            'title': 'Prepare BBQ',
            'content': 'Items:\n- Pork\n- Chicken',
        }, ensure_ascii=False))
        self.assertEqual(self.client.get('/api/notes').get_json(), notes_before)

    def test_requires_a_configured_api_key(self):
        with patch.dict(os.environ, {'OPENROUTER_API_KEY': ''}):
            with patch('src.routes.translate.urlopen') as urlopen:
                response = self.client.post('/api/translate', json={
                    'title': 'Hello', 'content': '', 'target_language': 'zh',
                })

        self.assertEqual(response.status_code, 503)
        urlopen.assert_not_called()

    def test_rejects_invalid_note_or_language(self):
        for payload in (
            {'title': '', 'content': '', 'target_language': 'zh'},
            {'title': 'Hello', 'content': '', 'target_language': 'fr'},
            {'title': 'Hello', 'content': '', 'target_language': []},
            {'title': 42, 'content': '', 'target_language': 'zh'},
        ):
            with self.subTest(payload=payload):
                self.assertEqual(self.client.post('/api/translate', json=payload).status_code, 400)

    def test_rejects_malformed_provider_response(self):
        provider_response = {'choices': [{'message': {'content': 'not JSON'}}]}
        provider_stream = io.BytesIO(json.dumps(provider_response).encode('utf-8'))
        with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'}):
            with patch('src.routes.translate.urlopen', return_value=provider_stream):
                response = self.client.post('/api/translate', json={
                    'title': 'Hello', 'content': 'World', 'target_language': 'zh',
                })

        self.assertEqual(response.status_code, 502)

    def test_retries_once_when_provider_returns_no_text(self):
        empty_response = {'choices': [{'message': {'content': None}}]}
        translated = {'title': '购物清单', 'content': '买牛奶和面包。'}
        valid_response = {
            'choices': [{'message': {'content': json.dumps(translated, ensure_ascii=False)}}]
        }
        responses = [
            io.BytesIO(json.dumps(empty_response).encode('utf-8')),
            io.BytesIO(json.dumps(valid_response).encode('utf-8')),
        ]

        with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'}):
            with patch('src.routes.translate.urlopen', side_effect=responses) as urlopen:
                response = self.client.post('/api/translate', json={
                    'title': 'Shopping list',
                    'content': 'Buy milk and bread.',
                    'target_language': 'zh',
                })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), translated)
        self.assertEqual(urlopen.call_count, 2)

if __name__ == '__main__':
    unittest.main()
