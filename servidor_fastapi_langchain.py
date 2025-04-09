from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

app = FastAPI()

class Pergunta(BaseModel):
    texto: str

llm = ChatOpenAI(temperature=0)

prompt = PromptTemplate(
    input_variables=["pergunta"],
    template= 
    """
Você é um assistente de química. Responda à pergunta abaixo listando SOMENTE os símbolos dos elementos químicos envolvidos, separados por vírgula, sem explicações adicionais.

Pergunta: {pergunta}

Resposta:
"""
)

chain = LLMChain(llm=llm, prompt=prompt)

@app.post("/pergunta")
async def responder(pergunta: Pergunta):
    resposta = chain.run(pergunta.texto)
    elementos = resposta.strip().replace(" ", "")
    return { "elementos": elementos }
