# Chemical Equipment Parameter Visualizer

A hybrid Web and Desktop application for analyzing and visualizing chemical equipment parameters from CSV data.

## Project Overview
This project uses a single Django REST backend that parses CSV data and performs analytics using Pandas.
The same backend APIs are consumed by both a React web application and a PyQt5 desktop application.

## Features
- CSV upload and parsing
- Data analytics (total count, averages, equipment type distribution)
- Web visualization using React and Chart.js
- Desktop visualization using PyQt5 and Matplotlib
- History of last 5 uploaded datasets stored in SQLite

## Tech Stack
- Backend: Django, Django REST Framework, Pandas
- Web Frontend: React.js, Chart.js
- Desktop App: PyQt5, Matplotlib
- Database: SQLite

## How to Run

### Backend
cd BACKEND/backend_project
venv\Scripts\activate
python manage.py runserver

### Web Frontend
cd web-frontend
npm start

### Desktop App
cd DESKTOP APP
python app.py

## Sample Data
A sample CSV file (sample_equipment_data.csv) is used for testing and demo.

## Future Enhancements
- Add user authentication using Django authentication or DRF tokens
- Generate PDF reports for analytics summaries
