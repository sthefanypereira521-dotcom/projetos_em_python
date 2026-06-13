from pydantic import BaseModel, Field, EmailStr
from schemas.transacoes_schema import Transacoes


class ClienteComTransacoes(BaseModel):
    cliente_id: int
    nome: str 
    email: EmailStr
    tipo_conta: str
    saldo: float
    transacoes: list[Transacoes]
