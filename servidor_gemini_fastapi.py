# servidor_gemini_fastapi.py
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# Inicializa o app FastAPI
app = FastAPI()

# Modelo da requisição
class Pergunta(BaseModel):
    texto: str

# Configura a chave da API do Gemini
# Lembre-se de definir GEMINI_API_KEY como variável de ambiente
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Inicializa o modelo Gemini Pro
model = genai.GenerativeModel("gemini-pro")

@app.post("/pergunta")
async def responder(pergunta: Pergunta):
    prompt = f"""
    Você é um assistente de química. Responda à pergunta abaixo listando SOMENTE os símbolos dos elementos químicos relacionados, separados por vírgula. Não escreva explicações.

    Pergunta: {pergunta.texto}

    Resposta:
    """
    try:
        response = model.generate_content(prompt)
        elementos = response.text.strip().replace("\n", "").replace(" ", "")
        return {"elementos": elementos}
    except Exception as e:
        return {"erro": str(e)}
