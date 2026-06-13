from fastapi import FastAPI
from routes.clientes import router as clientes_router
from routes.contas import router as contas_router
from routes.transacoes import router as transacoes_router
from routes.auth_router import router as auth_router


app = FastAPI()


@app.get("/", tags=["home"])
def sistema():

    return {"mensagem": "sistema  online"}


app.include_router(clientes_router)
app.include_router(contas_router)
app.include_router(transacoes_router)
app.include_router(auth_router)
