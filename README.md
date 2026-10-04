# NoteTaker - Personal Note Management Application

A modern, responsive web application for managing personal notes with a beautiful user interface and full CRUD functionality.

## 🌟 Features

- **Create Notes**: Add new notes with titles and rich content
- **Edit Notes**: Update existing notes with real-time editing
- **Delete Notes**: Remove notes you no longer need
- **Search Notes**: Find notes quickly by searching titles and content
- **Auto-save**: Notes are automatically saved as you type
- **Translate Notes**: Translate a note's title and content into Chinese or English with OpenRouter, then review before saving
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations
- **Real-time Updates**: Instant feedback and updates

## 🚀 Live Demo

The application is deployed and accessible at: **https://3dhkilc88dkk.manus.space**

## 🛠 Technology Stack

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript (ES6+)**: Interactive functionality and API communication

### Backend
- **Python Flask**: Web framework for API endpoints
- **SQLAlchemy**: ORM for database operations
- **Flask-CORS**: Cross-origin resource sharing support

### Database
- **Supabase PostgreSQL**: Shared online database when `DATABASE_URL` is set
- **SQLite**: Local fallback when `DATABASE_URL` is not set

## 📁 Project Structure

```
notetaking-app/
├── src/
│   ├── models/
│   │   ├── user.py          # User model (template)
│   │   └── note.py          # Note model with database schema
│   ├── routes/
│   │   ├── user.py          # User API routes (template)
│   │   ├── note.py          # Note API endpoints
│   │   └── translate.py     # Translation endpoint
│   ├── static/
│   │   ├── index.html       # Frontend application
│   │   └── favicon.ico      # Application icon
│   └── main.py              # Flask application entry point
├── database/
│   └── app.db               # SQLite database file, created on first run
├── .venv/                   # Python virtual environment
├── tests/                   # Translation endpoint tests
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Installation Steps

1. **Clone or download the project**
   ```bash
   python3.12 -m venv .venv
   ```

2. **Activate the virtual environment**
   ```bash
   source .venv/bin/activate
   ```

   Remark: On Windows, use `.venv\Scripts\activate`

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Supabase (optional for local development)**
   Open `.env` and set `DATABASE_URL` to the **Transaction pooler → URI** from Supabase's **Connect** dialog.
   Replace `[YOUR-PASSWORD]` in Supabase's URI with your database password. If the password contains URI special characters such as `@`, `#`, `/`, or `?`, percent-encode them before inserting it. The `.env` file is ignored by Git; never commit or share the full URI. If you leave `DATABASE_URL` unset, the app uses local SQLite instead. Existing SQLite notes are not copied to Supabase automatically.

5. **Run the application**
   Set your OpenRouter API key in `.env` (do not commit this file):
   ```dotenv
   OPENROUTER_API_KEY=your_openrouter_api_key
   OPENROUTER_MODEL=qwen/qwen3.8-27b:free
   ```
   The free Qwen model is the default; `OPENROUTER_MODEL` can override it. Set the same OpenRouter variables in Vercel when deploying.
   ```bash
   python src/main.py
   ```

6. **Access the application**
   - Open your browser and go to `http://localhost:5001`

## 📡 API Endpoints

### Notes API
- `GET /api/notes` - Get all notes
- `POST /api/notes` - Create a new note
- `GET /api/notes/<id>` - Get a specific note
- `PUT /api/notes/<id>` - Update a note
- `DELETE /api/notes/<id>` - Delete a note
- `GET /api/notes/search?q=<query>` - Search notes
- `POST /api/translate` - Translate editor text without saving it; accepts `title`, `content`, and `target_language` (`zh` or `en`)

The translation endpoint sends the title and content to OpenRouter. It returns translated `title` and `content` fields; the browser leaves the saved note unchanged until you click **Save**.

### Request/Response Format
```json
{
  "id": 1,
  "title": "My Note Title",
  "content": "Note content here...",
  "created_at": "2025-09-03T11:26:38.123456",
  "updated_at": "2025-09-03T11:27:30.654321"
}
```

## 🎨 User Interface Features

### Sidebar
- **Search Box**: Real-time search through note titles and content
- **New Note Button**: Create new notes instantly
- **Notes List**: Scrollable list of all notes with previews
- **Note Previews**: Show title, content preview, and last modified date

### Editor Panel
- **Title Input**: Edit note titles
- **Content Textarea**: Rich text editing area
- **Save Button**: Manual save option (auto-save also available)
- **Delete Button**: Remove notes with confirmation
- **Real-time Updates**: Changes reflected immediately

### Design Elements
- **Gradient Background**: Beautiful purple gradient backdrop
- **Glass Morphism**: Semi-transparent panels with backdrop blur
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Adapts to different screen sizes
- **Modern Typography**: Clean, readable font stack

## 🔒 Database Schema

### Notes Table
```sql
CREATE TABLE note (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 Deployment

To deploy on Vercel, import this GitHub repository as a new project and keep the project root as the Root Directory. The Flask entry point is `api/index.py`; `vercel.json` routes the site and API requests to it. Set these environment variables in Vercel for the Production environment before deploying:

- `DATABASE_URL`: Supabase Transaction pooler URI. This is required for persistent notes on Vercel.
- `OPENROUTER_API_KEY`: OpenRouter key for translation.
- `OPENROUTER_MODEL`: `qwen/qwen3.8-27b:free` (optional; this is already the default).

Copy the values from your local `.env` into Vercel's Environment Variables settings. Do not upload `.env` or commit the keys to Git. After deploying, check the public URL, `/api/notes`, and a translation. Disable Vercel's **Require log in** deployment protection if the exercise requires a public link.

This app currently has no sign-in or per-user note separation. Anyone who can open the public URL can read, edit, and delete notes in the connected database; use a database meant for the public exercise.

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` for debug mode
- `SECRET_KEY`: Flask secret key for sessions
- `OPENROUTER_API_KEY`: Required for translation
- `OPENROUTER_MODEL`: Optional model override; defaults to `qwen/qwen3.8-27b:free`
- `DATABASE_URL`: Supabase Transaction pooler URI; leave unset to use local SQLite. Configure the same variable in Vercel's project environment settings when deploying.

### Database Configuration
- Database file without `DATABASE_URL`: `database/app.db`
- Automatic table creation on first run
- SQLAlchemy ORM for database operations

## 📱 Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the browser console for error messages
2. Verify the Flask server is running
3. Ensure all dependencies are installed
4. Check network connectivity for the deployed version

## 🎯 Future Enhancements

Potential improvements for future versions:
- User authentication and multi-user support
- Note categories and tags
- Rich text formatting (bold, italic, lists)
- File attachments
- Export functionality (PDF, Markdown)
- Dark/light theme toggle
- Offline support with service workers
- Note sharing capabilities

---

**Built with ❤️ using Flask, SQLite, and modern web technologies**
