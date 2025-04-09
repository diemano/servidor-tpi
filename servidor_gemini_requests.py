# servidor_gemini_requests.py
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class Pergunta(BaseModel):
    texto: str

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.post("/pergunta")
async def responder(pergunta: Pergunta):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Responda à pergunta listando APENAS os símbolos dos elementos químicos, separados por vírgula. Sem explicações.\n\nPergunta: {pergunta.texto}\n\nResposta:"
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        data = response.json()

        if "candidates" in data:
            resposta_texto = data["candidates"][0]["content"]["parts"][0]["text"]
            elementos = resposta_texto.strip().replace("\n", "").replace(" ", "")
            return {"elementos": elementos}
        else:
            return {"erro": data.get("error", {}).get("message", "Erro desconhecido")}

    except Exception as e:
        return {"erro": str(e)}
