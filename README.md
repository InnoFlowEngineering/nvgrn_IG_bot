# Instagram Admin Bot - Demo (Prerelease)

A Python-based Instagram admin bot with a Tkinter UI and FastAPI backend. This is a **prerelease demo** with no actual API/LLM calls - all functionality is stubbed for demonstration purposes.

## Features

### 🎨 Tkinter UI
- **Three tabs**: Create, Scheduled, Posted
- **Create form** with:
  - Account selection (3 accounts: nvgrn_main, nvgrn_events, nvgrn_shop)
  - Upload type selection (post/reel/story)
  - Post type selection (dress/event/follow-up/post-event/other)
  - Event fields (name, date, location)
  - Context text area
  - Optional publish date picker
  - Save as draft or schedule functionality

### 🚀 FastAPI Backend
- RESTful API with stub endpoints
- In-memory post storage
- Webhook endpoint (stub)
- Scheduler stubs for scheduled posts
- Content moderation rules
- Interactive API documentation at `/docs`

### 🛡️ Content Moderation Rules
Automatic flagging for:
- ❌ Negative comments/refund requests (flag + hide, no replies)
- ❌ Competitor mentions (flag)
- ❌ Conflict indicators (flag)

## Project Structure

```
nvgrn_IG_bot/
├── src/
│   ├── api/                    # FastAPI backend
│   │   ├── __init__.py
│   │   ├── app.py              # Main API application
│   │   ├── store.py            # In-memory storage
│   │   └── scheduler.py        # Scheduler stubs
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   └── post.py             # Post model and enums
│   ├── ui/                     # Tkinter UI
│   │   ├── __init__.py
│   │   └── app.py              # Main UI application
│   └── utils/                  # Utilities
│       ├── __init__.py
│       └── rules.py            # Content moderation rules
├── output/                     # Output folder tree
│   ├── scheduled/              # Scheduled posts
│   ├── posted/                 # Posted content
│   └── drafts/                 # Draft posts
├── run_api.py                  # Script to run the API server
├── run_ui.py                   # Script to run the UI
├── demo.py                     # API demo script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/InnoFlowEngineering/nvgrn_IG_bot.git
cd nvgrn_IG_bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Note: Tkinter usually comes pre-installed with Python. If not available:
- Ubuntu/Debian: `sudo apt-get install python3-tk`
- macOS: Included with Python
- Windows: Included with Python

## Usage

### Running the Complete System

**Option 1: Separate terminals (recommended for development)**

Terminal 1 - Start the API server:
```bash
python3 run_api.py
```
The API will be available at http://localhost:8000
API documentation: http://localhost:8000/docs

Terminal 2 - Start the UI:
```bash
python3 run_ui.py
```

**Option 2: API Demo (no UI)**

Run the demo script to test API functionality:
```bash
python3 demo.py
```

### Using the UI

1. **Create Tab**: 
   - Fill in the form to create a new post
   - Select account, upload type, and post type
   - Add event details if applicable
   - Enter context/caption
   - Optionally set a publish date
   - Click "Save as Draft" or "Schedule"

2. **Scheduled Tab**:
   - View all scheduled posts
   - Click "Refresh" to update the list

3. **Posted Tab**:
   - View all posted content
   - Click "Refresh" to update the list

### API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /posts` - List all posts (with optional filters)
- `POST /posts` - Create a new post
- `GET /posts/{post_id}` - Get specific post
- `PUT /posts/{post_id}` - Update a post
- `DELETE /posts/{post_id}` - Delete a post
- `POST /posts/{post_id}/publish` - Publish a post
- `POST /webhook` - Webhook endpoint (stub)
- `GET /accounts` - List available accounts
- `GET /stats` - Get statistics

Full API documentation available at http://localhost:8000/docs when running the server.

## Content Moderation Rules

The system automatically checks content against predefined rules:

### Negative/Refund Keywords
Posts containing words like "refund", "scam", "fraud", "terrible", "disappointed" are:
- ⚠️ Flagged automatically
- 🚫 Hidden from public view
- 🔇 No replies allowed

### Competitor Keywords
Posts mentioning competitors or alternatives are:
- ⚠️ Flagged for review

### Conflict Keywords
Posts containing "controversy", "lawsuit", "dispute", "violation" are:
- ⚠️ Flagged for manual review

## Demo Limitations (Prerelease)

This is a **demonstration/prerelease version**. The following features are stubbed:

- ❌ No actual Instagram API integration
- ❌ No real post publishing
- ❌ No actual scheduling (APScheduler stub)
- ❌ No file uploads/media handling
- ❌ No LLM/AI integration
- ❌ In-memory storage only (data lost on restart)
- ❌ No authentication/authorization
- ❌ No database persistence

## Development

### Running in Development Mode

The API server runs with auto-reload enabled by default:
```bash
python3 run_api.py
```

### Adding New Features

1. **Models**: Add to `src/models/`
2. **API Endpoints**: Add to `src/api/app.py`
3. **UI Components**: Modify `src/ui/app.py`
4. **Rules**: Modify `src/utils/rules.py`

## Future Enhancements

- [ ] Actual Instagram API integration
- [ ] Database persistence (PostgreSQL/MongoDB)
- [ ] File upload and media handling
- [ ] Real-time scheduling with APScheduler
- [ ] User authentication
- [ ] AI-powered content suggestions
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] Webhook event processing

## License

MIT License (or your preferred license)

## Contributing

This is a demo project. For production use, significant enhancements would be required.

## Support

For issues or questions, please open an issue on GitHub.