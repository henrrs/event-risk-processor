import os
import json
from google.cloud import pubsub_v1
from app.models import GenAIResponse

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
OUTPUT_TOPIC = os.getenv("OUTPUT_TOPIC")
publisher = pubsub_v1.PublisherClient()

async def publish_to_output_topic(client_id: str, response: GenAIResponse):
    message = json.dumps({
        "client_id": client_id,
        "response": response.dict()
    }).encode("utf-8")
    topic_path = publisher.topic_path(PROJECT_ID, OUTPUT_TOPIC)
    publisher.publish(topic_path, message)
