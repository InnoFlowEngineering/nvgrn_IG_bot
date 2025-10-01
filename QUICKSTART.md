# Quick Start Guide

Get up and running with Instagram Admin Bot in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Tkinter (usually comes with Python)

## Installation

```bash
# Clone the repository
git clone https://github.com/InnoFlowEngineering/nvgrn_IG_bot.git
cd nvgrn_IG_bot

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

### Option 1: Full System (API + UI)

**Terminal 1** - Start the API:
```bash
python3 run_api.py
```

Wait for: `Application startup complete.`

**Terminal 2** - Start the UI:
```bash
python3 run_ui.py
```

### Option 2: API Demo Only

```bash
# Make sure API is running first
python3 demo.py
```

## Quick Test

### Test the API
```bash
# In another terminal while API is running
curl http://localhost:8000/health
```

Expected output:
```json
{
  "status": "healthy",
  "timestamp": "2024-XX-XXTXX:XX:XX",
  "posts_count": 0
}
```

### Test Content Rules
```bash
python3 test_rules.py
```

Expected: All 10 tests pass ✅

## Your First Post

1. Open the UI (`python3 run_ui.py`)
2. Go to "Create" tab
3. Fill in:
   - Account: nvgrn_main
   - Upload Type: Post
   - Post Type: other
   - Context: "Hello from Instagram Admin Bot! 🎉"
4. Click "Save as Draft"
5. See "Draft saved" in status bar ✅

## View Your Posts

1. Make sure API is running
2. Visit: http://localhost:8000/posts
3. Or in Python:
```python
import requests
response = requests.get("http://localhost:8000/posts")
print(response.json())
```

## API Documentation

While API is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Common Issues

### "Cannot connect to API"
**Problem**: UI can't reach the backend

**Solution**: Make sure API is running first
```bash
python3 run_api.py
```

### "ModuleNotFoundError: No module named 'tkinter'"
**Problem**: Tkinter not installed

**Solution**:
- Ubuntu/Debian: `sudo apt-get install python3-tk`
- macOS: Included with Python
- Windows: Included with Python

### "Address already in use"
**Problem**: Port 8000 is taken

**Solution**: Kill the existing process or change port in `run_api.py`

## What's Next?

- Read [UI_GUIDE.md](UI_GUIDE.md) for detailed UI documentation
- Read [README.md](README.md) for full feature list
- Check API docs at http://localhost:8000/docs
- Run the demo script to see all features

## Folder Structure

```
nvgrn_IG_bot/
├── src/              # Source code
│   ├── api/          # FastAPI backend
│   ├── models/       # Data models
│   ├── ui/           # Tkinter UI
│   └── utils/        # Utilities & rules
├── output/           # Output folders
├── run_api.py        # Start API server
├── run_ui.py         # Start UI
└── demo.py           # API demo
```

## Testing Features

### Test Content Moderation
Create a post with: "I want a refund for this terrible product"
- Should be flagged automatically ⚠️

### Test Scheduling
1. Create a post with publish date: `2024-12-31 23:59`
2. Click "Schedule"
3. Check "Scheduled" tab - post should appear

### Test Multiple Accounts
Create posts for all three accounts:
- nvgrn_main
- nvgrn_events
- nvgrn_shop

## Support

For issues, check:
1. Is API running? Check http://localhost:8000/health
2. Are dependencies installed? Run `pip install -r requirements.txt`
3. Check the console for error messages

---

**Remember**: This is a demo/prerelease version. No actual Instagram API calls are made!
