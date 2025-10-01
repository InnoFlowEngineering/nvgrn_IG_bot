#!/usr/bin/env python3
"""
Run the FastAPI backend server.
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Instagram Admin Bot API...")
    print("📍 API will be available at http://localhost:8000")
    print("📖 API docs available at http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(
        "src.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
