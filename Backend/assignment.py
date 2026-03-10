from sqlalchemy.orm import Session
from models import Agent

def assign_agent(db: Session):

    agents = db.query(Agent).all()

    if not agents:
        return None

    agent = min(agents, key=lambda x: x.active_leads)

    agent.active_leads += 1

    db.commit()

    return agent.agent_id


def round_robin_assignment(db):

    agents = db.execute("SELECT agent_id FROM agents").fetchall()

    last_lead = db.execute(
        "SELECT assigned_agent FROM leads ORDER BY lead_id DESC LIMIT 1"
    ).fetchone()

    if last_lead is None:
        return agents[0][0]

    agent_ids = [a[0] for a in agents]

    index = agent_ids.index(last_lead[0])

    next_index = (index + 1) % len(agent_ids)

    return agent_ids[next_index]


def workload_assignment(db):

    agent = db.execute(
        "SELECT agent_id FROM agents ORDER BY active_leads ASC LIMIT 1"
    ).fetchone()

    return agent[0]