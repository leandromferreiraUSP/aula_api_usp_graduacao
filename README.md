# Aula API USP Graduação

Este projeto propõe a construção de uma API básica como aula para a graduação em Engenharia de Computação da Poli USP, desenvolvida utilizando FastAPI, SQLAlchemy e PostgreSQL.

## Configurações e Execução do Projeto

### Docker para PostgreSQL

Para iniciar um contêiner Docker com PostgreSQL, execute o seguinte comando:

```sh
docker run --name postgressql -e POSTGRES_PASSWORD=1234 -p 5432:5432 -d postgres 
```

## Conexão com o Banco de Dados

Utilize a seguinte string de conexão para se conectar ao banco de dados PostgreSQL:

```java
jdbc:postgresql://localhost:5432/postgres?user=postgres&password=1234
```

## Poetry - Ambiente Virtual para Python

Para configurar o ambiente virtual utilizando Poetry, siga os passos abaixo:

1. Instale as dependências do projeto (na raiz do projeto).

```sh
poetry install
```

2. Adicione as dependências necessárias.

```sh
poetry add fastapi uvicorn sqlalchemy alembic psycopg2-binary requests
```

3. Ative o ambiente virtual.

```sh
poetry shell
```

## Comandos Alembic - ORM Python

Para gerenciar as migrações do banco de dados utilizando Alembic, siga os passos abaixo:

1. Ative o ambiente virtual.
```sh
poetry shell
```
2. Execute o comando Python abaixo para criar a base de dados:
```sh
python templates/create_db.py
```

3. Inicialize o Alembic.
```sh
alembic init alembic
```

4. Sobrescreva o arquivo padrão `env.py` com as configurações necessárias.
```sh
cp -f templates/env.py alembic/env.py 
```

5. Gere uma nova revisão do Alembic.
```sh
alembic revision --autogenerate -m "v0.0.1 - Criando Tabelas no Schema API" 
```

6. Aplique as migrações.
```sh
alembic upgrade head
```


## Executando a Aplicação

Para executar a aplicação, utilize o comando abaixo:
1. Na raiz do projeto ative o ambiente virtual poetry
```sh
poetry shell
```

2. Ative o servidor de API uvicorn
```sh
uvicorn app:app --reload --port 8000
```

## Debugging

Para debugar a aplicação, você pode rodar o arquivo **run_api.py** no modo de depuração do VSCode.

## Endpoints Disponíveis

- **POST /registro/**: Insere um novo registro.
- **GET /registros/**: Retorna todos os registros.
- **GET /registros/{id_registro}**: Retorna um registro específico pelo ID.
- **GET /registros/cidade/{id_cidade}**: Retorna um registro específico pelo ID da cidade e, opcionalmente, pela área.


### Diretório requests_api

O diretório **requests_api** contém scripts Python que realizam chamadas às APIs para diferentes operações. Aqui está uma descrição de cada arquivo e como utilizá-los:


*client_requests* - Este arquivo contém uma função para inserir um novo registro na API.
*create_registro.py* - Este arquivo contém uma função para inserir um novo registro na API.
*create_registro_batch.py*  - Este arquivo contém uma função para inserir registros em lotes via API.
*delete_registro.py* - Este arquivo contém uma função para deletar um registro específico pelo ID.
*get_registro_by_id.py* - Este arquivo contém uma função para obter um registro específico pelo ID.
*get_registro_cidade.py* - Este arquivo contém duas funções para obter um registro específico pelo ID da cidade e, opcionalmente, pela área.
*get_registros.py* - Este arquivo contém uma função para obter todos os registros.
*search_by_visitados.py* - Este arquivo contém uma função para buscar registros com base em um critério específico (por exemplo, visitados).  

  

Para executar os testes, basta rodar os arquivos Python correspondentes no diretório client_requests, ou depurar via seu VSCode:
```sh
python client_requests/create_registro_batch.py
python client_requests/create_registro.py
python client_requests/delete_registro.py
python client_requests/get_registro_by_id.py
python client_requests/get_registro_cidade.py
python client_requests/get_registros.py
python client_requests/search_by_visitados.py
```

## Contribuição

Sinta-se à vontade para contribuir com este projeto. Para isso, siga os passos abaixo:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Faça o push para a branch (`git push origin feature/nova-feature`).
5. Crie um novo Pull Request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

