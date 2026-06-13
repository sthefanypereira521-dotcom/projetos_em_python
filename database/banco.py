import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

conexao = sqlite3.connect(ROOT_PATH / "banco.sqlite3")
cursor = conexao.cursor()


def criar_tabela(conexao, cursor):
    cursor.execute()

    conexao.commit()

    conexao.close()


def inserir_dados(cursor, conexao):
    cursor.execute()

    conexao.commit()

    conexao.close()


def atualizar_dados():
    cursor.execute()

    conexao.commit()
    cursor.close()
    conexao.close()


def depositando():
    cursor.execute()
    conexao.commit()
    conexao.close()


def buscar(cursor):
    cursor.execute("""
        SELECT  clientes.id,transacoes.id,transacoes.tipo,transacoes.valor
        FROM clientes
        LEFT JOIN contas
        ON contas.cliente_id = clientes.id
        LEFT JOIN transacoes
        ON transacoes.conta_id = contas.id
        WHERE clientes.id = 3
                """)

    conexao.commit()
    conexao.close()


buscar(cursor)