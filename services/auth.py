from jose.constants import ALGORITHMS, Algorithms
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException
from jose import jwt, JWTError
from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def gerar_hash(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(
        senha_normal: str,
        senha_hash: str
):
    return pwd_context.verify(
        senha_normal,
        senha_hash
    )


def criar_token(dados: dict):
    dados_copia = dados.copy()

    expiracao = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    dados_copia.update({
        "exp": expiracao
    })

    token = jwt.encode(
        dados_copia,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token


def verificar_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="token invalido"
        )
