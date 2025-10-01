"""
Tkinter UI for Instagram Admin Bot.
Three tabs: Scheduled, Posted, Create
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from typing import Optional
import requests
import json


class IGBotUI:
    """Main UI class for Instagram Admin Bot."""
    
    def __init__(self, root: tk.Tk, api_url: str = "http://localhost:8000"):
        self.root = root
        self.api_url = api_url
        self.root.title("Instagram Admin Bot - Demo")
        self.root.geometry("900x700")
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_tab = ttk.Frame(self.notebook)
        self.scheduled_tab = ttk.Frame(self.notebook)
        self.posted_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.create_tab, text="Create")
        self.notebook.add(self.scheduled_tab, text="Scheduled")
        self.notebook.add(self.posted_tab, text="Posted")
        
        # Setup each tab
        self.setup_create_tab()
        self.setup_scheduled_tab()
        self.setup_posted_tab()
        
        # Status bar
        self.status_bar = tk.Label(
            root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_create_tab(self):
        """Setup the Create tab with the form."""
        # Main frame with scrollbar
        canvas = tk.Canvas(self.create_tab)
        scrollbar = ttk.Scrollbar(self.create_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        frame = scrollable_frame
        
        # Title
        title = tk.Label(frame, text="Create New Post", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10, sticky='w')
        
        # Account selection
        tk.Label(frame, text="Account:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.account_var = tk.StringVar(value="nvgrn_main")
        account_frame = ttk.Frame(frame)
        account_frame.grid(row=1, column=1, sticky='w', pady=5)
        
        accounts = ["nvgrn_main", "nvgrn_events", "nvgrn_shop"]
        for acc in accounts:
            ttk.Radiobutton(
                account_frame,
                text=acc,
                variable=self.account_var,
                value=acc
            ).pack(side=tk.LEFT, padx=5)
        
        # Upload type
        tk.Label(frame, text="Upload Type:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.upload_type_var = tk.StringVar(value="post")
        upload_frame = ttk.Frame(frame)
        upload_frame.grid(row=2, column=1, sticky='w', pady=5)
        
        upload_types = [("Post", "post"), ("Reel", "reel"), ("Story", "story")]
        for text, value in upload_types:
            ttk.Radiobutton(
                upload_frame,
                text=text,
                variable=self.upload_type_var,
                value=value
            ).pack(side=tk.LEFT, padx=5)
        
        # Post type
        tk.Label(frame, text="Post Type:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.post_type_var = tk.StringVar(value="other")
        post_types = ["dress", "event", "follow-up", "post-event", "other"]
        post_type_combo = ttk.Combobox(
            frame,
            textvariable=self.post_type_var,
            values=post_types,
            state="readonly",
            width=30
        )
        post_type_combo.grid(row=3, column=1, sticky='w', pady=5)
        
        # Event fields section
        tk.Label(frame, text="Event Details (optional):", font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=2, sticky='w', padx=10, pady=(15, 5))
        
        # Event name
        tk.Label(frame, text="Event Name:").grid(row=5, column=0, sticky='w', padx=10, pady=5)
        self.event_name_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.event_name_var, width=40).grid(row=5, column=1, sticky='w', pady=5)
        
        # Event date
        tk.Label(frame, text="Event Date:").grid(row=6, column=0, sticky='w', padx=10, pady=5)
        self.event_date_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.event_date_var, width=40).grid(row=6, column=1, sticky='w', pady=5)
        tk.Label(frame, text="(Format: YYYY-MM-DD)", font=("Arial", 8)).grid(row=6, column=2, sticky='w', padx=5)
        
        # Event location
        tk.Label(frame, text="Event Location:").grid(row=7, column=0, sticky='w', padx=10, pady=5)
        self.event_location_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.event_location_var, width=40).grid(row=7, column=1, sticky='w', pady=5)
        
        # Context
        tk.Label(frame, text="Context:", font=("Arial", 10, "bold")).grid(row=8, column=0, sticky='nw', padx=10, pady=5)
        self.context_text = scrolledtext.ScrolledText(frame, width=50, height=10)
        self.context_text.grid(row=8, column=1, sticky='w', pady=5)
        
        # Publish date
        tk.Label(frame, text="Publish Date (optional):", font=("Arial", 10, "bold")).grid(row=9, column=0, sticky='w', padx=10, pady=5)
        self.publish_date_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.publish_date_var, width=40).grid(row=9, column=1, sticky='w', pady=5)
        tk.Label(frame, text="(Format: YYYY-MM-DD HH:MM)", font=("Arial", 8)).grid(row=9, column=2, sticky='w', padx=5)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=10, column=0, columnspan=3, pady=20)
        
        ttk.Button(
            button_frame,
            text="Save as Draft",
            command=self.save_draft
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Schedule",
            command=self.schedule_post
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form
        ).pack(side=tk.LEFT, padx=5)
    
    def setup_scheduled_tab(self):
        """Setup the Scheduled tab to view scheduled posts."""
        # Title
        title = tk.Label(self.scheduled_tab, text="Scheduled Posts", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Refresh button
        ttk.Button(
            self.scheduled_tab,
            text="Refresh",
            command=self.refresh_scheduled
        ).pack(pady=5)
        
        # Treeview for posts
        columns = ("ID", "Account", "Type", "Post Type", "Publish Date", "Flagged")
        self.scheduled_tree = ttk.Treeview(
            self.scheduled_tab,
            columns=columns,
            show='headings',
            height=20
        )
        
        for col in columns:
            self.scheduled_tree.heading(col, text=col)
            self.scheduled_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.scheduled_tab,
            orient=tk.VERTICAL,
            command=self.scheduled_tree.yview
        )
        self.scheduled_tree.configure(yscroll=scrollbar.set)
        
        self.scheduled_tree.pack(side=tk.LEFT, fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill='y', pady=10)
        
        # Load initial data
        self.refresh_scheduled()
    
    def setup_posted_tab(self):
        """Setup the Posted tab to view posted content."""
        # Title
        title = tk.Label(self.posted_tab, text="Posted Content", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Refresh button
        ttk.Button(
            self.posted_tab,
            text="Refresh",
            command=self.refresh_posted
        ).pack(pady=5)
        
        # Treeview for posts
        columns = ("ID", "Account", "Type", "Post Type", "Created", "Flagged")
        self.posted_tree = ttk.Treeview(
            self.posted_tab,
            columns=columns,
            show='headings',
            height=20
        )
        
        for col in columns:
            self.posted_tree.heading(col, text=col)
            self.posted_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.posted_tab,
            orient=tk.VERTICAL,
            command=self.posted_tree.yview
        )
        self.posted_tree.configure(yscroll=scrollbar.set)
        
        self.posted_tree.pack(side=tk.LEFT, fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill='y', pady=10)
        
        # Load initial data
        self.refresh_posted()
    
    def save_draft(self):
        """Save post as draft."""
        try:
            post_data = self.get_form_data()
            post_data['status'] = 'draft'
            
            response = requests.post(f"{self.api_url}/posts", json=post_data)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('flagged'):
                messagebox.showwarning(
                    "Post Flagged",
                    f"Draft saved but flagged:\n{result.get('flag_reason')}"
                )
            else:
                messagebox.showinfo("Success", "Draft saved successfully!")
            
            self.clear_form()
            self.update_status("Draft saved")
            
        except requests.exceptions.ConnectionError:
            messagebox.showerror(
                "Connection Error",
                "Cannot connect to API. Make sure the backend is running."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save draft: {str(e)}")
    
    def schedule_post(self):
        """Schedule a post for future publication."""
        try:
            post_data = self.get_form_data()
            
            if not post_data.get('publish_date'):
                messagebox.showerror("Error", "Publish date is required for scheduling")
                return
            
            post_data['status'] = 'scheduled'
            
            response = requests.post(f"{self.api_url}/posts", json=post_data)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('flagged'):
                messagebox.showwarning(
                    "Post Flagged",
                    f"Post scheduled but flagged:\n{result.get('flag_reason')}"
                )
            else:
                messagebox.showinfo("Success", "Post scheduled successfully!")
            
            self.clear_form()
            self.refresh_scheduled()
            self.update_status("Post scheduled")
            
        except requests.exceptions.ConnectionError:
            messagebox.showerror(
                "Connection Error",
                "Cannot connect to API. Make sure the backend is running."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule post: {str(e)}")
    
    def get_form_data(self) -> dict:
        """Get data from the form."""
        context = self.context_text.get("1.0", tk.END).strip()
        
        if not context:
            raise ValueError("Context is required")
        
        data = {
            'account': self.account_var.get(),
            'upload_type': self.upload_type_var.get(),
            'post_type': self.post_type_var.get(),
            'context': context
        }
        
        # Add optional fields if provided
        if self.event_name_var.get():
            data['event_name'] = self.event_name_var.get()
        
        if self.event_date_var.get():
            data['event_date'] = self.event_date_var.get()
        
        if self.event_location_var.get():
            data['event_location'] = self.event_location_var.get()
        
        if self.publish_date_var.get():
            # Convert to ISO format
            try:
                dt = datetime.strptime(self.publish_date_var.get(), "%Y-%m-%d %H:%M")
                data['publish_date'] = dt.isoformat()
            except ValueError:
                raise ValueError("Invalid publish date format. Use YYYY-MM-DD HH:MM")
        
        return data
    
    def clear_form(self):
        """Clear the create form."""
        self.account_var.set("nvgrn_main")
        self.upload_type_var.set("post")
        self.post_type_var.set("other")
        self.event_name_var.set("")
        self.event_date_var.set("")
        self.event_location_var.set("")
        self.context_text.delete("1.0", tk.END)
        self.publish_date_var.set("")
    
    def refresh_scheduled(self):
        """Refresh the scheduled posts list."""
        try:
            # Clear existing items
            for item in self.scheduled_tree.get_children():
                self.scheduled_tree.delete(item)
            
            # Fetch scheduled posts
            response = requests.get(f"{self.api_url}/posts?status=scheduled")
            response.raise_for_status()
            
            posts = response.json()
            
            for post in posts:
                self.scheduled_tree.insert('', 'end', values=(
                    post['id'][:8] + '...',
                    post['account'],
                    post['upload_type'],
                    post['post_type'],
                    post.get('publish_date', 'N/A')[:16] if post.get('publish_date') else 'N/A',
                    'Yes' if post.get('flagged') else 'No'
                ))
            
            self.update_status(f"Loaded {len(posts)} scheduled posts")
            
        except requests.exceptions.ConnectionError:
            self.update_status("Cannot connect to API")
        except Exception as e:
            self.update_status(f"Error loading scheduled posts: {str(e)}")
    
    def refresh_posted(self):
        """Refresh the posted content list."""
        try:
            # Clear existing items
            for item in self.posted_tree.get_children():
                self.posted_tree.delete(item)
            
            # Fetch posted content
            response = requests.get(f"{self.api_url}/posts?status=posted")
            response.raise_for_status()
            
            posts = response.json()
            
            for post in posts:
                self.posted_tree.insert('', 'end', values=(
                    post['id'][:8] + '...',
                    post['account'],
                    post['upload_type'],
                    post['post_type'],
                    post.get('created_at', 'N/A')[:16],
                    'Yes' if post.get('flagged') else 'No'
                ))
            
            self.update_status(f"Loaded {len(posts)} posted items")
            
        except requests.exceptions.ConnectionError:
            self.update_status("Cannot connect to API")
        except Exception as e:
            self.update_status(f"Error loading posted content: {str(e)}")
    
    def update_status(self, message: str):
        """Update the status bar."""
        self.status_bar.config(text=message)


def main():
    """Main entry point for the UI."""
    root = tk.Tk()
    app = IGBotUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
