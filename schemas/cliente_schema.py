from pydantic import BaseModel, EmailStr, Field


class Cliente(BaseModel):
    id: int
    nome: str 
    email: EmailStr


class ClienteCriar(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class ClienteUpdate(BaseModel):
    nome:str
    email:EmailStr
