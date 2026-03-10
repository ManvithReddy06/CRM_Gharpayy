from pydantic import BaseModel

class LeadCreate(BaseModel):
    name: str
    phone: str
    email: str
    source: str


class VisitCreate(BaseModel):
    lead_id: int
    property_name: str
    visit_date: str
    visit_time: str
    
    