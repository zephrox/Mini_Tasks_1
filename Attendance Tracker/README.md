# Attendance Tracker

A web-based application built with Python (Flask) and HTML/CSS to manage trainee attendance. It uses local CSV files for persistent data storage.

## Features
- **Register Trainee**: Register new trainees with a unique ID and Name.
- **Mark Attendance**: Select a date and mark attendance (Present/Absent) for each trainee.
- **Attendance Report**: View a table showing total days, present days, absent days, and attendance percentage.
- **Export**: Export the attendance report as a CSV file.

## Requirements
- Python 3
- Flask

## Installation and Execution
1. Install Flask:
   ```bash
   pip install Flask
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Access the web interface at `http://127.0.0.1:5000/`.

## Data Storage
The application uses two local CSV files, created automatically in the project directory upon the first execution:
- `trainees.csv`: Stores trainee IDs and Names.
- `attendance.csv`: Stores attendance records per trainee and date.
