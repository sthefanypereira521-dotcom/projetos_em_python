import sqlite3
from security import pwd_context
from services.auth import verificar_token
from schemas.transacoes_schema import Mensagem


from schemas.cliente_schema import (
    Cliente,
    ClienteCriar,
    ClienteUpdate)

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    security)


from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials)


router = APIRouter(
    prefix="/clientes",
    tags=["clientes"]

)

security = HTTPBearer()


@router.post("/", response_model=Cliente)
def criar_clientes(cliente: ClienteCriar,
                   credenciais: HTTPAuthorizationCredentials =
                   Depends(security)
                   ):
    payload = verificar_token(
        credenciais.credentials
    )
    """ Criando clientes  """

    senha_hash = pwd_context.hash(cliente.senha)

    conn = sqlite3.connect("database/banco.sqlite3")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
      INSERT INTO clientes(
        nome,
        email,
        senha
      )             
      VALUES(?, ?, ?)
    """,
                   (
                       cliente.nome,
                       cliente.email,
                       senha_hash
                   ))

    conn.commit()
    cliente_id = cursor.lastrowid
    conn.close()

    return {
        "id": cliente_id,
        "nome": cliente.nome,
        "email": cliente.email
    }


@router.get("/", response_model=list[Cliente])
def listar_clientes(
    credenciais: HTTPAuthorizationCredentials =
    Depends(security)
):
    payload = verificar_token(
        credenciais.credentials
    )
    """ listar todos clientes  """

    conn = sqlite3.connect("database/banco.sqlite3")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
      SELECT id, nome, email
      FROM clientes
  """)

    clientes = cursor.fetchall()
    conn.close()

    if not clientes:
        raise HTTPException(
            status_code=404,
            detail="cliente nao encontrado"
        )

    return [
        Cliente(
            id=c["id"],
            nome=c["nome"],
            email=c["email"]
        )

        for c in clientes
    ]


@router.patch("/{cliente_id}", response_model=ClienteUpdate)
def atualizar_cliente(cliente_id: int, cliente: Cliente,
                      credenciais: HTTPAuthorizationCredentials =
                      Depends(security)
                      ):
    payload = verificar_token(
        credenciais.credentials
    )
    """atualizando clientes """

    conn = sqlite3.connect("database/banco.sqlite3")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE clientes
        SET nome = ?, email = ?
        WHERE id = ?
        """,
                   (

                       cliente.nome,
                       cliente.email,
                       cliente_id
                   )
                   )
    conn.commit()

    return {
        "nome": cliente.nome,
        "email": cliente.email
    }


@router.delete("/{id}")
def deletar_cliente(
    id: int,
    credenciais: HTTPAuthorizationCredentials = Depends(security)
):
    verificar_token(credenciais.credentials)

    conn = sqlite3.connect("database/banco.sqlite3")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM clientes WHERE id = ?",
        (id,)
    )

    cliente = cursor.fetchone()

    if not cliente:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    cursor.execute(
        "DELETE FROM clientes WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return {
        "mensagem": f"Cliente {id} removido com sucesso"
    }
