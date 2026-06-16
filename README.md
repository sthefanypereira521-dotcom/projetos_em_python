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

git clone https://github.com/sthefanypereira521-dotcom/projetos_em_python.git
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


## Testando as rotas

**As rotas foram testadas com o Insomnia.**
O arquivo `insomnia_sistema_bancario_collection.yaml` 
está na raiz do projeto.

Para importar:
1. Abra o Insomnia
2. Clique em Import
3. Selecione o arquivo .yaml
4. Todas as rotas já estarão configuradas




##  Autora

***Sthefany***  
Desenvolvedora Backend em formação  
[GitHub](https://github.com/sthefanypereira521-dotcom/projetos_em_python) • [LinkedIn](https://www.linkedin.com/in/sthefany-pereira-dev)
