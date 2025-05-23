import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict
import base64

from fastapi import FastAPI, Request
from app.models import ClientEvent
from app.services.event_store import store_event, get_recent_events, store_audit_log
from app.services.prompt_builder import build_prompt
from app.services.genai_client import query_genai
from app.services.pubsub_client import publish_to_output_topic

# --- Inicializações --- #
app = FastAPI()

# --- Endpoint Pub/Sub Push --- #
@app.post("/events")
async def receive_event(request: Request):
    try:
        envelope = await request.json()
        if not envelope.get("message"):
            return JSONResponse(content={"status": "no message"}, status_code=200)

        data = json.loads(base64.b64decode(envelope["message"]["data"]).decode("utf-8"))
        event = ClientEvent(**data)

        await store_event(event)

        recent_events = await get_recent_events(event.client_id)
        prompt = build_prompt(recent_events)
        response = await query_genai(prompt)

        await publish_to_output_topic(event.client_id, response)
        await store_audit_log(event.client_id, recent_events, response)

        return JSONResponse(content={"status": "processed"}, status_code=200)

    except Exception as e:
        # Log do erro no stdout
        print(f"Error processing the event: {e}")
        return JSONResponse(content={"status": "error"}, status_code=200)

# --- Instruções para execução local --- #
# uvicorn app.main:app --host 0.0.0.0 --port 8080
