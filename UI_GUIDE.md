# Instagram Admin Bot - UI Guide

## Overview
The Instagram Admin Bot UI is built with Tkinter and provides a user-friendly interface for managing Instagram content across multiple accounts.

## Starting the UI

1. **Start the API server first** (in a separate terminal):
```bash
python3 run_api.py
```

2. **Start the UI**:
```bash
python3 run_ui.py
```

The UI will open in a new window with three tabs: Create, Scheduled, and Posted.

## UI Layout

### Main Window
- **Title**: Instagram Admin Bot - Demo
- **Size**: 900x700 pixels
- **Tabs**: Create, Scheduled, Posted
- **Status Bar**: Shows current operation status at the bottom

---

## Tab 1: Create

The Create tab contains a comprehensive form for creating new Instagram posts.

### Form Fields

#### 1. Account Selection (Required)
- **Type**: Radio buttons
- **Options**: 
  - nvgrn_main
  - nvgrn_events
  - nvgrn_shop
- **Default**: nvgrn_main
- **Description**: Select which Instagram account to post from

#### 2. Upload Type (Required)
- **Type**: Radio buttons
- **Options**:
  - Post (static image/carousel)
  - Reel (short video)
  - Story (temporary 24h content)
- **Default**: Post
- **Description**: Choose the type of content to upload

#### 3. Post Type (Required)
- **Type**: Dropdown/Combobox
- **Options**:
  - dress
  - event
  - follow-up
  - post-event
  - other
- **Default**: other
- **Description**: Categorize the post for analytics and organization

#### 4. Event Details (Optional Section)
These fields appear below the post type and are optional:

**Event Name**
- **Type**: Text input
- **Example**: "Summer Fashion Show 2024"
- **Description**: Name of the event being promoted

**Event Date**
- **Type**: Text input
- **Format**: YYYY-MM-DD
- **Example**: 2024-07-15
- **Description**: Date of the event

**Event Location**
- **Type**: Text input
- **Example**: "Downtown Gallery, 123 Main St"
- **Description**: Where the event takes place

#### 5. Context (Required)
- **Type**: Scrolled text area
- **Size**: 50 characters wide, 10 lines tall
- **Description**: The main caption/text for the post. This is where you write your message, hashtags, and content.
- **Content Moderation**: This field is automatically checked against content rules when saved.

#### 6. Publish Date (Optional)
- **Type**: Text input
- **Format**: YYYY-MM-DD HH:MM
- **Example**: 2024-07-15 14:30
- **Description**: Schedule the post for future publication. Leave empty to save as draft only.

### Action Buttons

**Save as Draft**
- Saves the post with status="draft"
- Validates required fields
- Applies content moderation rules
- Shows warning if content is flagged
- Clears form on success

**Schedule**
- Saves the post with status="scheduled"
- Requires publish_date to be filled
- Validates date format
- Applies content moderation rules
- Adds post to scheduler (stub)
- Shows warning if content is flagged
- Clears form on success
- Refreshes the Scheduled tab

**Clear Form**
- Resets all form fields to default values
- Does not save any data

### Content Moderation Warnings

When creating a post, the content is automatically checked against moderation rules:

- **Negative/Refund Keywords**: If detected, a warning appears stating the post is flagged and hidden with no replies allowed
- **Competitor Mentions**: If detected, a warning appears that the post is flagged for review
- **Conflict Keywords**: If detected, a warning appears that the post is flagged for review

The post is still saved/scheduled, but marked as flagged for manual review.

---

## Tab 2: Scheduled

The Scheduled tab displays all posts that have been scheduled for future publication.

### Layout
- **Refresh Button**: Updates the list with latest data from API
- **Table/Tree View**: Shows scheduled posts in a sortable table

### Columns
1. **ID**: Short version of post ID (first 8 characters + "...")
2. **Account**: Which account the post is for (nvgrn_main, nvgrn_events, nvgrn_shop)
3. **Type**: Upload type (post, reel, story)
4. **Post Type**: Category (dress, event, follow-up, etc.)
5. **Publish Date**: When the post is scheduled to be published (YYYY-MM-DD HH:MM)
6. **Flagged**: Yes/No indicator if content was flagged by moderation rules

### Features
- Scrollable list for many posts
- Auto-loads data when tab is opened
- Click Refresh to update with latest data
- Posts are sorted by created date (newest first)

---

## Tab 3: Posted

The Posted tab displays all content that has been published to Instagram.

### Layout
- **Refresh Button**: Updates the list with latest data from API
- **Table/Tree View**: Shows posted content in a sortable table

### Columns
1. **ID**: Short version of post ID (first 8 characters + "...")
2. **Account**: Which account the post was posted to
3. **Type**: Upload type (post, reel, story)
4. **Post Type**: Category (dress, event, follow-up, etc.)
5. **Created**: When the post was created (YYYY-MM-DD HH:MM)
6. **Flagged**: Yes/No indicator if content was flagged

### Features
- Scrollable list for many posts
- Auto-loads data when tab is opened
- Click Refresh to update with latest data
- Posts are sorted by created date (newest first)

---

## Status Bar

At the bottom of the window, a status bar shows:
- "Ready" when idle
- "Draft saved" after successfully saving
- "Post scheduled" after scheduling
- "Loaded X scheduled posts" after refreshing Scheduled tab
- "Loaded X posted items" after refreshing Posted tab
- Error messages if API connection fails

---

## Error Handling

### Connection Errors
If the API is not running, you'll see:
- **Error Dialog**: "Cannot connect to API. Make sure the backend is running."
- **Status Bar**: "Cannot connect to API"

**Solution**: Start the API server with `python3 run_api.py`

### Validation Errors
- **Missing Context**: "Context is required"
- **Invalid Publish Date**: "Invalid publish date format. Use YYYY-MM-DD HH:MM"
- **Missing Publish Date for Schedule**: "Publish date is required for scheduling"

### Flagged Content Warnings
When content violates moderation rules, a warning dialog appears but the post is still saved:
- Shows which rule was triggered
- Explains the action taken (flag, hide, no replies)
- Post is marked as flagged in the database

---

## Workflow Examples

### Example 1: Create a Simple Post
1. Open the UI (make sure API is running)
2. Go to "Create" tab
3. Select account: nvgrn_main
4. Select upload type: Post
5. Select post type: dress
6. Enter context: "Check out our new summer collection! 🌞 #fashion #summer"
7. Click "Save as Draft"
8. Success! Form clears and status shows "Draft saved"

### Example 2: Schedule a Post for Future
1. Go to "Create" tab
2. Fill in all fields as above
3. Set publish date: 2024-07-15 14:00
4. Click "Schedule"
5. Success! Post is scheduled and appears in "Scheduled" tab

### Example 3: Create an Event Post
1. Go to "Create" tab
2. Select account: nvgrn_events
3. Select upload type: Post
4. Select post type: event
5. Event name: "Summer Fashion Show"
6. Event date: 2024-07-15
7. Event location: "Downtown Gallery"
8. Context: "Join us for an exclusive fashion show! See the latest trends."
9. Click "Save as Draft"

### Example 4: View All Scheduled Posts
1. Go to "Scheduled" tab
2. See all posts scheduled for future publication
3. Click "Refresh" to update the list

---

## Tips & Best Practices

1. **Always run the API first** - The UI cannot function without the backend API
2. **Check the status bar** - It provides immediate feedback on operations
3. **Use the Refresh buttons** - Data is not automatically updated; click Refresh to see changes
4. **Watch for flagged content** - Pay attention to warning dialogs about content moderation
5. **Date formats matter** - Use the exact formats shown (YYYY-MM-DD for dates, YYYY-MM-DD HH:MM for timestamps)
6. **Clear form after reviewing flagged content** - If content is flagged, review the warning and decide whether to modify it

---

## Keyboard Navigation

- **Tab**: Move between form fields
- **Enter**: Submit forms (when in text inputs)
- **Escape**: Close dialog boxes
- Standard Tkinter shortcuts work throughout the UI

---

## Demo Mode Limitations

Remember this is a **prerelease demo**:
- ❌ No actual Instagram API calls
- ❌ Posts are not really published
- ❌ Scheduling is simulated
- ❌ No file/image uploads
- ❌ Data is stored in-memory only (lost on restart)

This is for demonstration and testing the workflow only.
