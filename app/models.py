from datetime import datetime
from typing import Dict
from pydantic import BaseModel

class ClientEvent(BaseModel):
    client_id: str
    event_type: str
    timestamp: datetime
    details: Dict

class GenAIResponse(BaseModel):
    risk_assessment: str
    suggested_action: str
    justification: str