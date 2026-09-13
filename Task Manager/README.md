# Task Manager

A simple Flask-based Task Manager application that allows you to create, edit, update, and delete tasks.
This version of the application stores all data locally in a `tasks.json` file.

## Features

- **Add Tasks**: Provide a title, description, deadline, and priority.
- **Edit Tasks**: Update any properties of existing tasks.
- **Update Status**: Quickly change task status (Pending, In Progress, Completed).
- **Filter**: Filter tasks by their current status.
- **Delete Tasks**: Remove tasks from the system.
- **JSON Storage**: Tasks are saved in a simple, readable JSON file (`tasks.json`).

## Setup Instructions

1. Ensure you have Python installed.
2. Install the required dependencies (Flask):
   ```bash
   pip install Flask
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Access the web interface at `http://127.0.0.1:5000`.

## File Structure

- `app.py`: The main Flask server application.
- `tasks.json`: The JSON database where all task information is stored (created automatically upon first run).
- `templates/`: Contains the HTML templates for the frontend (`index.html`, `edit.html`).
- `static/`: Contains static assets like CSS.
