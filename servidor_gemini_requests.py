from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# 🔓 CORS liberado para qualquer origem (ou especifique seu domínio GitHub Pages se quiser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["https://diemano.github.io"] para maior segurança
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Pergunta(BaseModel):
    texto: str

# 🔑 API KEY do Google AI Studio (Makersuite)
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
