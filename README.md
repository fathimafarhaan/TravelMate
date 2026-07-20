# 🌍 TravelMate

TravelMate is a full-stack travel management application built using **Flask**, **HTML**, **CSS**, **JavaScript**, **SQLite**, **MySQL**, and **Pandas**.

The application allows users to manage trips, places to visit, planning notes, travel expenses, and view analytical insights through an interactive dashboard.

---

## Features

- Manage Trips (Create, View, Update, Delete)
- Manage Places to Visit
- Manage Planning Notes
- Manage Travel Expenses
- Interactive Dashboard with Analytics
- SQLite support for Development & Testing
- MySQL support for Production
- Unit Testing using Python unittest
- Environment-based Database Configuration

---

## Tech Stack

### Backend
- Python
- Flask
- Pandas

### Frontend
- HTML
- CSS
- JavaScript

### Database
- SQLite
- MySQL

### Tools
- Git
- GitHub
- Virtual Environment
- python-dotenv

---

## Installation

Clone the repository.

```bash
git clone https://github.com/fathimafarhaan/TravelMate.git
cd TravelMate
```

Create and activate a virtual environment.

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

### Development (SQLite)

```bash
export APP_ENV=development
python app.py
```

### Production (MySQL)

```bash
export APP_ENV=production
python app.py
```

The application automatically selects the database based on the configured environment.

---

## Running Tests

```bash
python -m unittest discover tests
```

SQLite is used for testing to ensure the test suite runs consistently across different systems.

---

## Dashboard Analytics

The dashboard provides:

- Total Trips
- Completed Trips
- Planned Trips
- Total Expenses
- Travel Type Summary
- Expense Category Summary
- Country Summary
- Budget vs Expense
- Monthly Travel Trend
- Places Visited Summary

Analytics are implemented using **Pandas**.

---
