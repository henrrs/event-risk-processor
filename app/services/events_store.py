from datetime import datetime, timedelta
from typing import List
from google.cloud import firestore
from app.models import ClientEvent, GenAIResponse

db = firestore.Client()
EVENT_WINDOW_MINUTES = 5
FIRESTORE_COLLECTION = "risk_assessments"

async def store_event(event: ClientEvent):
    db.collection("client_events").add(event.dict())

async def get_recent_events(client_id: str) -> List[ClientEvent]:
    cutoff = datetime.utcnow() - timedelta(minutes=EVENT_WINDOW_MINUTES)
    query = db.collection("client_events") \
               .where("client_id", "==", client_id) \
               .where("timestamp", ">=", cutoff)
    docs = query.stream()
    return [ClientEvent(**doc.to_dict()) for doc in docs]

async def store_audit_log(client_id: str, events: List[ClientEvent], response: GenAIResponse):
    db.collection(FIRESTORE_COLLECTION).add({
        "client_id": client_id,
        "timestamp": firestore.SERVER_TIMESTAMP,
        "events": [e.dict() for e in events],
        "response": response.dict(),
    })
