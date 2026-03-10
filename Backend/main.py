from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

import models
import schemas

from database import SessionLocal
from assignment import assign_agent

app = FastAPI()


# ---------------- DATABASE CONNECTION ----------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- ACTIVITY LOGGER ----------------

def log_activity(db: Session, lead_id: int, activity: str):

    new_activity = models.Activity(
        lead_id=lead_id,
        activity=activity
    )

    db.add(new_activity)
    db.commit()


# ---------------- HOME ROUTE ----------------

@app.get("/")
def home():
    return {"message": "CRM API Running Successfully"}


# ---------------- CREATE LEAD ----------------

@app.post("/create-lead")
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):

    agent_id = assign_agent(db)

    new_lead = models.Lead(
        name=lead.name,
        phone=lead.phone,
        email=lead.email,
        source=lead.source,
        status="New Lead",
        assigned_agent=agent_id
    )

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    log_activity(db, new_lead.lead_id, "Lead Created")

    return {"message": "Lead Created Successfully"}


# ---------------- VIEW ALL LEADS ----------------

@app.get("/leads")
def get_leads(db: Session = Depends(get_db)):

    leads = db.query(models.Lead).all()

    return leads


# ---------------- UPDATE PIPELINE ----------------

@app.put("/update-status/{lead_id}")
def update_status(lead_id: int, status: str, db: Session = Depends(get_db)):

    lead = db.query(models.Lead).filter(models.Lead.lead_id == lead_id).first()

    if not lead:
        return {"error": "Lead not found"}

    lead.status = status
    db.commit()

    log_activity(db, lead_id, f"Status changed to {status}")

    return {"message": "Lead pipeline updated successfully"}


# ---------------- SCHEDULE VISIT ----------------

@app.post("/schedule-visit")
def schedule_visit(visit: schemas.VisitCreate, db: Session = Depends(get_db)):

    new_visit = models.Visit(
        lead_id=visit.lead_id,
        property_name=visit.property_name,
        visit_date=visit.visit_date,
        visit_time=visit.visit_time,
        outcome="Pending"
    )

    db.add(new_visit)
    db.commit()

    log_activity(db, visit.lead_id, "Visit Scheduled")

    return {"message": "Visit scheduled successfully"}


# ---------------- UPDATE VISIT OUTCOME ----------------

@app.put("/update-visit-outcome")
def update_visit_outcome(lead_id: int, outcome: str, db: Session = Depends(get_db)):

    visit = db.query(models.Visit).filter(
        models.Visit.lead_id == lead_id
    ).first()

    if not visit:
        return {"error": "Visit not found for this lead"}

    visit.outcome = outcome
    db.commit()

    log_activity(db, lead_id, f"Visit outcome updated to {outcome}")

    return {"message": "Visit outcome updated successfully"}

# ---------------- FOLLOW-UP REMINDER ----------------

@app.get("/followups")
def get_followups(db: Session = Depends(get_db)):

    one_day_ago = datetime.utcnow() - timedelta(days=1)

    leads = db.query(models.Lead).filter(
        models.Lead.created_at <= one_day_ago,
        models.Lead.status == "New Lead"
    ).all()

    return leads


# ---------------- DASHBOARD METRICS ----------------

@app.get("/total-leads")
def total_leads(db: Session = Depends(get_db)):

    count = db.query(models.Lead).count()

    return {"total_leads": count}


@app.get("/pipeline-stats")
def pipeline_stats(db: Session = Depends(get_db)):

    stages = [
        "New Lead",
        "Contacted",
        "Requirement Collected",
        "Property Suggested",
        "Visit Scheduled",
        "Visit Completed",
        "Booked",
        "Lost"
    ]

    stats = {}

    for stage in stages:
        count = db.query(models.Lead).filter(models.Lead.status == stage).count()
        stats[stage] = count

    return stats


@app.get("/total-visits")
def total_visits(db: Session = Depends(get_db)):

    count = db.query(models.Visit).count()

    return {"visits": count}


@app.get("/bookings")
def bookings(db: Session = Depends(get_db)):

    count = db.query(models.Lead).filter(models.Lead.status == "Booked").count()

    return {"bookings": count}


# ---------------- LEAD ACTIVITY TIMELINE ----------------

@app.get("/lead-activity/{lead_id}")
def lead_activity(lead_id: int, db: Session = Depends(get_db)):

    activities = db.query(models.Activity).filter(
        models.Activity.lead_id == lead_id
    ).all()

    return activities


# ---------------- AGENT PERFORMANCE LEADERBOARD ----------------

from sqlalchemy import func

@app.get("/agent-leaderboard")
def agent_leaderboard(db: Session = Depends(get_db)):

    agents = db.query(models.Agent).all()

    data = []

    for agent in agents:

        leads_handled = db.query(models.Lead).filter(
            models.Lead.assigned_agent == agent.agent_id
        ).count()

        bookings = db.query(models.Lead).filter(
            models.Lead.assigned_agent == agent.agent_id,
            models.Lead.status == "Booked"
        ).count()

        data.append({
            "Agent": agent.name,
            "Leads Handled": leads_handled,
            "Bookings": bookings
        })

    return data