from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from database import Base

class Agent(Base):
    __tablename__ = "agents"

    agent_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    active_leads = Column(Integer)


class Lead(Base):
    __tablename__ = "leads"

    lead_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    source = Column(String(50))
    status = Column(String(50))
    assigned_agent = Column(Integer, ForeignKey("agents.agent_id"))
    created_at = Column(DateTime, default=datetime.utcnow)


class Visit(Base):
    __tablename__ = "visits"

    visit_id = Column(Integer, primary_key=True)
    lead_id = Column(Integer)
    property_name = Column(String(100))
    visit_date = Column(String(50))
    visit_time = Column(String(50))
    outcome = Column(String(50))
    
    
    
class Activity(Base):
    __tablename__ = "activities"

    activity_id = Column(Integer, primary_key=True)
    lead_id = Column(Integer)
    activity = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)    