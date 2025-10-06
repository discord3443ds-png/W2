from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
import json

# FastAPI App
app = FastAPI()  # MUSS exakt "app" heißen

# OpenRouter Key aus Environment Variable
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_KEY,
)

# Request Model
class GenRequest(BaseModel):
    prompt: str

# Endpoint
@app.post("/generate")
def generate(req: GenRequest):
    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3.1:free",
            messages=[{"role":"user", "content": req.prompt}]
        )

        response_content = completion.choices[0].message.content

        # JSON zurückgeben
        data = json.loads(response_content)
        return data

    except Exception as e:
        return {"error": str(e), "raw": response_content if 'response_content' in locals() else ""}
