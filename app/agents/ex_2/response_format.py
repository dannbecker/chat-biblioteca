from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from app.agents.models import llm_gemini_flash
from app.agents.ex_2.sql_constructor import gerar_consulta_sql

template = """
Você é um agente cujo trabalho é receber uma pergunta que o usuário fez, receber os dados que estão associados à pergunta dele num formato de lista e formatar um texto sucinto, mas explicativo e humanizado, referente aos dados dessa lista. 

Observações gerias: 
* Seja mais direto e sem muito exagero na sua resposta. 
* Se for necessário para complementar sua resposta, considere o histórico de conversa que está recebendo também.
* No histórico de conversa, você vai receber também o resultado da consulta SQL obtido naquela interação anterior para ser usado de contexto. Utilize-o caso o usuário pergunte algo que você precise user de um dado anterior.
Atenção: Retire todo e qualquer markdown que vier na resposta, deixe apenas texto cru.

Aqui está o que ele perguntou:
{pergunta}
Aqui está a resposta:
{resultado}

Aqui está o histórico de conversa:
{historico}
"""

def gerar_resposta(pergunta, historico):
    prompt = PromptTemplate(
        template=template,
        input_variables=["pergunta", "resultado"]
    )

    consulta_sql = gerar_consulta_sql(pergunta)

    prompt_format = prompt.format(pergunta=pergunta, resultado=consulta_sql, historico=historico)
    resposta = llm_gemini_flash.invoke([HumanMessage(content=prompt_format)])
    print(resposta.content)
    return resposta.content, consulta_sql