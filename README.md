# 🏠 Gharpayy CRM System

A full-stack **Customer Relationship Management (CRM)** system built for real estate lead management. It features a **FastAPI** backend with a **MySQL** database and a **Streamlit** frontend dashboard — designed to help sales agents capture, track, and convert property leads efficiently.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Features](#-features)
- [Database Schema](#-database-schema)
- [API Endpoints](#-api-endpoints)
- [Agent Assignment Logic](#-agent-assignment-logic)
- [Setup & Installation](#-setup--installation)
- [Running the App](#-running-the-app)
- [Screenshots](#-screenshots)
- [Future Improvements](#-future-improvements)

---

## 🧩 Overview

Gharpayy CRM is built to streamline the end-to-end sales pipeline for a PG/property rental business. It supports:

- Automatic lead assignment to agents based on workload
- Multi-stage pipeline tracking (New Lead → Booked / Lost)
- Property visit scheduling and outcome tracking
- Activity timeline for every lead
- Agent performance leaderboard
- Follow-up reminder system for stale leads

---

## 🛠 Tech Stack

| Layer       | Technology                          |
|-------------|--------------------------------------|
| Backend     | Python, FastAPI, SQLAlchemy          |
| Database    | MySQL (via PyMySQL)                  |
| Frontend    | Streamlit                            |
| ORM         | SQLAlchemy (Declarative Base)        |
| Validation  | Pydantic (Schemas)                   |
| Server      | Uvicorn (ASGI)                       |

---

## 📁 Project Structure

```
gharpayy-crm/
│
├── backend/
│   ├── main.py              # FastAPI app — all API routes
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── database.py          # DB engine, session, Base setup
│   └── assignment.py        # Agent assignment logic
│
├── frontend/
│   ├── dashboard.py         # Main Streamlit CRM dashboard
│   └── lead_capture.py      # Standalone lead capture form
│
└── README.md
```

---

## ✨ Features

### 🔹 Lead Management
- Create new leads with name, phone, email, and source
- View all leads in a tabular format
- Move leads through an 8-stage pipeline

### 🔹 Pipeline Stages
```
New Lead → Contacted → Requirement Collected → Property Suggested
→ Visit Scheduled → Visit Completed → Booked → Lost
```

### 🔹 Visit Scheduling
- Schedule property visits with date and time
- Supports multiple Gharpayy PG locations
- Update visit outcomes: Interested / Not Interested / Booked / Needs More Options

### 🔹 Follow-up Reminders
- Automatically surfaces leads that are still in "New Lead" status after 24 hours
- Helps agents prioritize outreach

### 🔹 Activity Timeline
- Tracks every action taken on a lead (creation, status changes, visits)
- Displayed as a visual timeline in the dashboard

### 🔹 Agent Leaderboard
- Ranks agents by total leads handled and bookings confirmed
- Visualized via bar chart and metric cards

### 🔹 Dashboard Metrics
- Total Leads
- Visits Scheduled
- Bookings Confirmed
- Pipeline stage breakdown (table + bar chart)

---

## 🗄 Database Schema

### `agents`
| Column        | Type         | Description                  |
|---------------|--------------|------------------------------|
| agent_id      | INT (PK)     | Unique agent identifier       |
| name          | VARCHAR(100) | Agent's full name             |
| email         | VARCHAR(100) | Agent's email address         |
| active_leads  | INT          | Current number of active leads|

### `leads`
| Column         | Type         | Description                        |
|----------------|--------------|------------------------------------|
| lead_id        | INT (PK)     | Unique lead identifier              |
| name           | VARCHAR(100) | Lead's full name                    |
| phone          | VARCHAR(20)  | Lead's phone number                 |
| email          | VARCHAR(100) | Lead's email address                |
| source         | VARCHAR(50)  | Lead source (Website, WhatsApp etc) |
| status         | VARCHAR(50)  | Current pipeline stage              |
| assigned_agent | INT (FK)     | References `agents.agent_id`        |
| created_at     | DATETIME     | Timestamp of lead creation          |

### `visits`
| Column        | Type         | Description                   |
|---------------|--------------|-------------------------------|
| visit_id      | INT (PK)     | Unique visit identifier        |
| lead_id       | INT          | Associated lead                |
| property_name | VARCHAR(100) | Name of the property visited   |
| visit_date    | VARCHAR(50)  | Date of the visit              |
| visit_time    | VARCHAR(50)  | Time of the visit              |
| outcome       | VARCHAR(50)  | Result of the visit            |

### `activities`
| Column      | Type         | Description                      |
|-------------|--------------|----------------------------------|
| activity_id | INT (PK)     | Unique activity identifier        |
| lead_id     | INT          | Associated lead                   |
| activity    | VARCHAR(255) | Description of the activity       |
| created_at  | DATETIME     | Timestamp of the activity         |

---

## 🔌 API Endpoints

### General
| Method | Endpoint     | Description              |
|--------|--------------|--------------------------|
| GET    | `/`          | Health check             |

### Leads
| Method | Endpoint                      | Description                      |
|--------|-------------------------------|----------------------------------|
| POST   | `/create-lead`                | Create a new lead                |
| GET    | `/leads`                      | Fetch all leads                  |
| PUT    | `/update-status/{lead_id}`    | Update lead's pipeline stage     |
| GET    | `/followups`                  | Get leads needing follow-up      |

### Visits
| Method | Endpoint                  | Description                        |
|--------|---------------------------|------------------------------------|
| POST   | `/schedule-visit`         | Schedule a property visit          |
| PUT    | `/update-visit-outcome`   | Update outcome of a visit          |

### Dashboard & Analytics
| Method | Endpoint                    | Description                         |
|--------|-----------------------------|-------------------------------------|
| GET    | `/total-leads`              | Count of all leads                  |
| GET    | `/total-visits`             | Count of all visits                 |
| GET    | `/bookings`                 | Count of booked leads               |
| GET    | `/pipeline-stats`           | Lead count per pipeline stage       |
| GET    | `/lead-activity/{lead_id}`  | Activity timeline for a lead        |
| GET    | `/agent-leaderboard`        | Agent performance rankings          |

---

## 🤖 Agent Assignment Logic

Defined in `assignment.py`, three strategies are implemented:

### 1. `assign_agent()` — Minimum Workload (Active)
Assigns the lead to the agent with the **fewest active leads** currently. After assignment, increments that agent's `active_leads` counter.

```python
agent = min(agents, key=lambda x: x.active_leads)
agent.active_leads += 1
```

### 2. `round_robin_assignment()` — Round Robin
Cycles through agents in order. Finds the last assigned agent and picks the next one in the list.

### 3. `workload_assignment()` — SQL-Based Workload
Uses a raw SQL query to find the agent with the fewest active leads:
```sql
SELECT agent_id FROM agents ORDER BY active_leads ASC LIMIT 1
```

> **Currently active:** `assign_agent()` (minimum workload strategy) is used in `main.py`.

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.9+
- MySQL Server running locally
- pip

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/gharpayy-crm.git
cd gharpayy-crm
```

### 2. Install Dependencies
```bash
pip install fastapi uvicorn sqlalchemy pymysql streamlit requests pandas pydantic
```

### 3. Configure the Database

Update `database.py` with your MySQL credentials:
```python
DATABASE_URL = "mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost/crm_db"
```

Then create the database in MySQL:
```sql
CREATE DATABASE crm_db;
```

### 4. Initialize Tables

Run the following once to create all tables:
```python
# In a Python shell or add temporarily to main.py
from database import engine
import models
models.Base.metadata.create_all(bind=engine)
```

---

## 🚀 Running the App

### Start the Backend (FastAPI)
```bash
cd backend
uvicorn main:app --reload
```
API will be live at: `http://127.0.0.1:8000`

Auto-generated docs available at: `http://127.0.0.1:8000/docs`

### Start the Frontend (Streamlit Dashboard)
```bash
cd frontend
streamlit run dashboard.py
```

### Start the Lead Capture Form (Optional)
```bash
streamlit run lead_capture.py
```

---

## 🖼 Screenshots

> _Add screenshots of your dashboard, pipeline view, leaderboard, and activity timeline here._

| Dashboard | Pipeline Update | Agent Leaderboard |
|-----------|----------------|-------------------|
| ![dashboard](#) | ![pipeline](#) | ![leaderboard](#) |

---

## 🔮 Future Improvements

- [ ] JWT-based authentication for agents and admins
- [ ] Email / WhatsApp notification on lead assignment
- [ ] Role-based access control (Admin vs Agent view)
- [ ] Export leads to CSV / Excel
- [ ] Lead scoring based on engagement
- [ ] Integration with external lead sources (Google Forms, IndiaMART)
- [ ] Mobile-responsive frontend (React / Next.js)
- [ ] Dockerize the full stack for easy deployment

---

## 👨‍💻 Author

Built with ❤️ for **Gharpayy** — making PG rentals smarter, one lead at a time.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
