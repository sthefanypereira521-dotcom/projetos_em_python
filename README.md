# Sistema Bancário — API REST

API de sistema bancário desenvolvida com FastAPI e SQLite, com autenticação JWT.  
Projeto de portfólio construído para praticar desenvolvimento backend com Python.



##  Tecnologias

- Python 3.11
- FastAPI
- SQLite3
- JWT (autenticação)




##  Funcionalidades

- Cadastro e gerenciamento de clientes
- Criação e consulta de contas bancárias
- Depósito e saque com validação de saldo
- Extrato de transações por cliente
- Autenticação com token JWT




###  Como rodar localmente

**Clone o repositório**

git clone https://github.com/seu-usuario/sistema-bancario.git
cd sistema-bancario


**Instale as dependências com Poetry**
**poetry install**


### Rode o servidor

**poetry run uvicorn main:app --reload**


**Acesse a documentação interativa**

http://localhost:8000/docs




##  Autenticação

**As rotas protegidas exigem token JWT no header**


Authorization: Bearer <seu_token>
Obtenha o token na rota  POST /auth/token com email e senha.




##  Autora

***Sthefany***  
Desenvolvedora Backend em formação  
[GitHub](https://github.com/seu-usuario) • [LinkedIn](https://linkedin.com/in/seu-perfil)
