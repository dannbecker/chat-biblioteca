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
Você é um agente cujo trabalho é receber uma pergunta que o usuário fez, receber os dados que estão associados à pergunta dele num formato de lista e formatar um texto sucinto, mas explicativo e humanizado, referente aos dados dessa lista. 

Observações gerias: Seja mais direto e sem muito exagero na sua resposta.
Atenção: Retire todo e qualquer markdown que vier na resposta, deixe apenas texto cru.

Aqui está o que ele perguntou:
{pergunta}
Aqui está a resposta:
{resultado}
"""

def gerar_resposta(pergunta):
    prompt = PromptTemplate(
        template=template,
        input_variables=["pergunta", "resultado"]
    )

    consulta_sql = gerar_consulta_sql(pergunta)

    prompt_format = prompt.format(pergunta=pergunta, resultado=consulta_sql)
    resposta = llm_gemini_flash.invoke([HumanMessage(content=prompt_format)])

    return resposta.content