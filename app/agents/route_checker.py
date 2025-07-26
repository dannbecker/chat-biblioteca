import json
from database import engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from app.agents.schema import schema
from app.agents.models import llm_gemini_flash, llm_gemini_pro
from app.agents.sql_constructor import gerar_consulta_sql

template = """
{pergunta}
{openapi}
"""

def verificar_rota(pergunta):
    prompt = PromptTemplate(
        template=template,
        input_variables=["pergunta", "openapi"]
    )

    with open('openapi.json', 'r', encoding='utf-8') as file:
        openapi = file.read()


    prompt_format = prompt.format(pergunta=pergunta, openapi=openapi)
    resposta = llm_gemini_flash.invoke([HumanMessage(content=prompt_format)])

    return resposta.content