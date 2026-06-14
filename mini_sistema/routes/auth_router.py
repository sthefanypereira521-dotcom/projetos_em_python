import sqlite3
from schemas.login_schema import Login

from fastapi import (
    APIRouter,
    HTTPException)


from services.auth import (
    verificar_senha,
    criar_token
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
def login(dados: Login):

    conn = sqlite3.connect("database/banco.sqlite3")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes WHERE email = ? ", (dados.email,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()

    if not cliente:
        raise HTTPException(status_code=401,
                            detail="email ou senha invalidos")

    senha_correta = verificar_senha(dados.senha, cliente["senha"])

    if not senha_correta:
        raise HTTPException(status_code=401,
                            detail="email ou senha invalidos")

    token = criar_token({
        "sub": cliente["email"],
        "id": cliente["id"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

