from datetime import datetime, timedelta, timezone
from typing import List
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from app.models import ClientEvent, GenAIResponse

db = firestore.Client()
EVENT_WINDOW_MINUTES = 5
FIRESTORE_COLLECTION = "risk_assessments"

async def store_event(event: ClientEvent):
    db.collection("client_events").add(event.dict())

async def get_recent_events(client_id: str) -> List[ClientEvent]:
    client_events_ref = db.collection("client_events")

    print(client_events_ref)

    cutoff = datetime.now(timezone.utc) - timedelta(minutes=EVENT_WINDOW_MINUTES)

    print(cutoff)

    docs = client_events_ref.where(
            filter=FieldFilter("client_id", "==", client_id)
        ).where(filter=FieldFilter("timestamp", ">=", cutoff)).stream()

    print(docs)

    return [ClientEvent(**doc.to_dict()) for doc in docs]

async def store_audit_log(client_id: str, events: List[ClientEvent], response: GenAIResponse):
    db.collection(FIRESTORE_COLLECTION).add({
        "client_id": client_id,
        "timestamp": firestore.SERVER_TIMESTAMP,
        "events": [e.dict() for e in events],
        "response": response.dict(),
    })
