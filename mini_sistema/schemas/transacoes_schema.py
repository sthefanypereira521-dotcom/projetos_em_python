
from pydantic import BaseModel


class Mensagem(BaseModel):
    mensagem: str


class Transacoes(BaseModel):
    tipo: str
    valor: float


