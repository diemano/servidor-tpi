from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class Pergunta(BaseModel):
    texto: str

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={API_KEY}"

@app.post("/pergunta")
async def responder(pergunta: Pergunta):
    prompt = f"""
    Responda com os símbolos dos elementos químicos mencionados na pergunta abaixo. Apenas os símbolos, separados por vírgula. Não explique.

    Pergunta: {pergunta.texto}
    """

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GEMINI_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        elementos = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        return {"elementos": elementos}
    except Exception as e:
        return {"erro": str(e)}
