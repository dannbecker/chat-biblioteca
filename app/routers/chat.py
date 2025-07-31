from fastapi import APIRouter, status
from pydantic import BaseModel
from app.agents.ex_2.response_format import gerar_resposta

router = APIRouter(prefix="/chat", tags=["Chat"])
class ChatQuestion(BaseModel):
    mensagem: str

class ChatResponse(BaseModel):
    resposta: str

@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK, summary="Enviar nova Mensagem de Consulta")
def enviar_mensagem(pergunta: ChatQuestion):
    resposta = gerar_resposta(pergunta.mensagem)
    return {
        "resposta": resposta
    }
