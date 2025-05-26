import os
from openai import OpenAI
from app.models import GenAIResponse

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def query_genai(prompt: str) -> GenAIResponse:
    completion = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    content = completion.choices[0].message.content
    lines = content.strip().split("\n")
    return GenAIResponse(
        risk_assessment=lines[0],
        suggested_action=lines[1].split(":")[-1].strip(),
        justification=" ".join(lines[2:])
    )
