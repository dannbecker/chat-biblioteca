from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from app.agents.models import llm_gemini_flash

template = """
Você é um agente especialista em APIs REST e OpenAPI. Sua tarefa é analisar a pergunta do usuário e identificar as rotas da API mais relevantes para responder à solicitação.

### Você receberá:

1. A pergunta do usuário
2. A especificação da API no formato OpenAPI 3.0 (YAML ou JSON)

### O que você deve fazer:

* Identifique quais endpoints (path + method) atendem à solicitação.

* Liste apenas parâmetros não-body (query, path, header, cookie) em parameters.

### Para métodos com corpo (POST/PUT/PATCH, e qualquer rota com requestBody):

* Localize requestBody.content["application/json"].schema.

* Se houver $ref, resolva o $ref recursivamente em components.schemas.

* Expanda composições (allOf, oneOf, anyOf).

* Para allOf: faça o merge de required e properties.

* Para oneOf/anyOf: liste variações em alternatives, cada uma com seus requiredFields.

* Se o schema for um array, resolva items (incluindo $ref em items).

* Extraia a lista final de campos obrigatórios (requiredFields) e descreva os campos em bodyFields (nome, tipo, descrição, se é obrigatório).

* Caso o schema esteja inline (sem $ref), use-o diretamente.

* Se requestBody.required estiver ausente, considere required=false.

* Prefira application/json; se inexistente, use o primeiro content disponível e informe o contentType usado.

* Formato de saída: retorne somente o JSON a seguir (nada de texto fora do JSON).

### Template de saída exemplo:

```json
[
  {{
    "path": "/exemplo/de/rota/get",
    "method": "GET",
    "description": "Descrição da finalidade da rota",
    "parameters": [
      {{
        "name": "search",
        "in": "query",
        "required": false,
        "type": "string",
        "description": "Termo de busca"
      }},
      {{
        "name": "id",
        "in": "path",
        "required": true,
        "type": "integer",
        "description": "ID do recurso"
      }}
    ]
  }},
  {{
    "path": "/exemplo/de/rota/post",
    "method": "POST",
    "description": "Descrição da finalidade da rota",
    "parameters": [
      {{
        "name": "id",
        "in": "path",
        "required": true,
        "type": "integer",
        "description": "ID do recurso"
      }}
    ],
    "requestBody": {{
      "required": true,
      "contentType": "application/json",
      "schemaRef": "#/components/schemas/UserCreate",
      "requiredFields": ["email", "password"],
      "bodyFields": [
        {{
          "name": "email",
          "type": "string",
          "required": true,
          "description": "E-mail do usuário"
        }},
        {{
          "name": "password",
          "type": "string",
          "required": true,
          "description": "Senha do usuário"
        }},
        {{
          "name": "name",
          "type": "string",
          "required": false,
          "description": "Nome do usuário"
        }}
      ],
      "alternatives": []
    }}
  }}
]
```

### Observações importantes
* Não coloque campos do body dentro de parameters; parameters é só para query/path/header/cookie.

* Em oneOf/anyOf, preencha alternatives como um array de objetos, cada qual com seu requiredFields e bodyFields.

* Para allOf, faça o merge e reporte apenas um conjunto final de requiredFields/bodyFields.

* Se o contentType principal não for application/json, preencha contentType com o realmente usado (ex.: multipart/form-data) e siga a mesma lógica.

### Input do usuário:

Pergunta:
{pergunta}

Documentação Openapi:
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

#resposta = verificar_rota(pergunta="Quero criar um livro com o nome Programação para Iniciantes")

# print(resposta)