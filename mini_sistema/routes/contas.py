import sqlite3
from services.auth import verificar_token

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    security)


from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials)

from schemas.contas_schema import (
    Conta,
    Conta_resposta,
    Criar_Conta)


router = APIRouter(
    prefix="/contas",
    tags=["contas"]
)

security = HTTPBearer()


@router.post("/", response_model=Conta_resposta)
def criando_conta(conta: Criar_Conta,
                  credenciais: HTTPAuthorizationCredentials =
                  Depends(security)
                  ):
    payload = verificar_token(
        credenciais.credentials
    )

    """ criando contas... """

    conn = sqlite3.connect("database/banco.sqlite3")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO contas(
            numero_conta,
            tipo_conta,
            saldo,
            cliente_id
        )
        VALUES(?, ?, ?, ?) 
                     
        """,
                   (
                       conta.numero_conta,
                       conta.tipo_conta,
                       conta.saldo,
                       conta.cliente_id
                   )
                   )

    conn.commit()

    id_conta = cursor.lastrowid

    cursor.execute(
        "SELECT * FROM contas WHERE id = ?", (id_conta,)
    )

    nova_conta = cursor.fetchone()
    conn.close()

    return dict(nova_conta)


@router.get("/")
def listar_contas(
    credenciais: HTTPAuthorizationCredentials =
    Depends(security)
):
    payload = verificar_token(
        credenciais.credentials
    )
    """ listando todas as contas"""

    conn = sqlite3.connect("database/banco.sqlite3")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contas")

    contas = cursor.fetchall()
    conn.close()

    if contas is None:
        raise HTTPException(
            status_code=404,
            detail="contas nao encontradas"
        )

    return {"contas": contas}


@router.get("/{conta_id}", response_model=Conta)
def buscar_conta(conta_id: int,
                 credenciais: HTTPAuthorizationCredentials =
                 Depends(security)
                 ):

    payload = verificar_token(
        credenciais.credentials
    )

    """ listar conta expecifica  """

    conn = sqlite3.connect("database/banco.sqlite3")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, saldo  
        FROM contas 
        WHERE id = ? """, (conta_id,))

    conta = cursor.fetchone()
    conn.close()

    if conta is None:
        raise HTTPException(
            status_code=404,
            detail="conta nao encontrada"
        )

    return Conta(
        id=conta["id"],
        saldo=conta["saldo"]
    )


