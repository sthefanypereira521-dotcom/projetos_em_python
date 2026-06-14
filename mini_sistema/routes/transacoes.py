import sqlite3
from schemas.cliente_completo_schema import ClienteComTransacoes
from services.auth import verificar_token


from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    security)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials)

from schemas.transacoes_schema import (
    Transacoes,
    Mensagem)


router = APIRouter(
    prefix="/transacoes",
    tags=["transacoes"]
)

security = HTTPBearer()


@router.post("/deposito", response_model=Mensagem)
def realizar_deposito(
    conta_id: int,
    valor: float,
    credenciais: HTTPAuthorizationCredentials =
    Depends(security)
):
    payload = verificar_token(
        credenciais.credentials
    )

    """ realiza depositos"""

    conn = sqlite3.connect("database/banco.sqlite3")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM contas
         WHERE id = ?
        """, (conta_id,)
    )

    conta = cursor.fetchone()

    if conta is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Conta não encontrada"
        )

    if valor <= 0:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="valor deve ser maio que zero"
        )

    cursor.execute("""
        UPDATE contas
        SET saldo = saldo + ?
        WHERE id = ?
        """, (valor, conta_id)
    )

    cursor.execute("""
        INSERT INTO  transacoes(tipo, valor, conta_id)
        VALUES(?, ?, ?)
    """, ("deposito", valor, conta_id))

    conn.commit()
    conn.close()

    return {
        "mensagem": "deposito realizado",
        "conta_id": conta_id,
        "tipo": "deposito",
        "valor": valor
    }


@router.post("/saque", response_model=Mensagem)
def realizar_saque(
    conta_id: int,
    valor: float,
    credenciais: HTTPAuthorizationCredentials =
    Depends(security)
):
    payload = verificar_token(
        credenciais.credentials
    )

    """ realiza saques """

    conn = sqlite3.connect("database/banco.sqlite3")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT saldo
        FROM contas
        WHERE id = ?
        """,
        (conta_id,)
    )

    conta = cursor.fetchone()

    if conta is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Conta não encontrada"
        )

    saldo_atual = conta[0]

    if saldo_atual < valor:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="saldo insuficiente"
        )

    cursor.execute(
        """
        UPDATE contas
        SET saldo = saldo - ?
        WHERE id = ?
        """,
        (valor, conta_id)
    )

    cursor.execute("""
        INSERT INTO transacoes(tipo, valor, conta_id)
        VALUES(?,?,?)
    """, ("saque", valor, conta_id))

    conn.commit()
    conn.close()

    return {
        "mensagem": "Saque realizado",
        "conta_id": conta_id,
        "tipo": "saque",
        "valor": valor,
        "saldo_restante": saldo_atual - valor
    }


@router.get("/contas/clientes/", response_model=list[ClienteComTransacoes])
def listar_transaçoes(
    credenciais: HTTPAuthorizationCredentials = Depends(security)
):
    payload = verificar_token(
        credenciais.credentials
    )

    cliente_id = payload["id"]

    """ lista clientes contas e transaçoes """

    conn = sqlite3.connect("database/banco.sqlite3")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            clientes.id,
            clientes.nome,
            clientes.email,
            contas.tipo_conta,
            contas.saldo,
            transacoes.id,
            transacoes.tipo,
            transacoes.valor
            

        FROM clientes

        LEFT JOIN contas
        ON contas.cliente_id = clientes.id

        LEFT JOIN transacoes
        ON transacoes.conta_id = contas.id

        WHERE clientes.id = ?

        ORDER BY transacoes.id
        """, (cliente_id,))

    dados = cursor.fetchall()
    conn.close()

    resultado = {}

    for item in dados:

        cliente_id = item[0]

        if cliente_id not in resultado:

            resultado[cliente_id] = {
                "cliente_id": item[0],
                "nome": item[1],
                "email": item[2],
                "tipo_conta": item[3],
                "saldo": item[4],
                "transacoes": []
            }
        if item[5] is not None:
            resultado[cliente_id]["transacoes"].append(
                {
                    "id": item[5],
                    "tipo": item[6],
                    "valor": item[7]


                }
            )
    
    return list(resultado.values())


@router.get("/")
def todas_transaçoes(
    credenciais: HTTPAuthorizationCredentials = Depends(security)
):
    payload = verificar_token(
        credenciais.credentials
    )
    cliente_id = payload["id"]

    conn = sqlite3.connect("database/banco.sqlite3")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
         id,
         conta_id,
         tipo,
         valor
        FROM transacoes
        WHERE conta_id = ?          
        ORDER BY transacoes.id
    """, (cliente_id,))

    dados = cursor.fetchall()
    conn.close()

    return [dict(item)for item in dados]
