from typing import List
from app.models import ClientEvent

def build_prompt(events: List[ClientEvent]) -> str:
    prompt = "Considere os seguintes eventos recentes de um cliente:\n"
    for event in events:
        prompt += f"- [{event.timestamp}] {event.event_type}: {event.details}\n"
    prompt += (
        "\nAnalise o risco e forneça:\n"
        "1. Avaliação textual de risco\n"
        "2. Sugestão de ação (monitorar, alertar, bloquear)\n"
        "3. Justificativa interpretável"
    )
    return prompt
