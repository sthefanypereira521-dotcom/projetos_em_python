
from pydantic import BaseModel


class Conta(BaseModel):
    id: int
    saldo: float


class Criar_Conta(BaseModel):
    numero_conta: str
    tipo_conta: str
    saldo: float
    cliente_id: int


class Conta_resposta(BaseModel):
    id: int
    numero_conta: str
    tipo_conta: str
    saldo: float
    cliente_id: int
