#!/usr/bin/env python3
"""
Run the Tkinter UI application.
"""
import sys
import tkinter as tk
from src.ui.app import IGBotUI

if __name__ == "__main__":
    print("🎨 Starting Instagram Admin Bot UI...")
    print("📍 Make sure the API is running at http://localhost:8000")
    print("\nClose the window to exit\n")
    
    root = tk.Tk()
    app = IGBotUI(root)
    root.mainloop()
