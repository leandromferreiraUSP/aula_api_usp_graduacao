# Database

O componente Database é responsável por gerenciar a conexão e interações com o banco de dados PostgreSQL. Ele fornece a base para todas as operações de persistência de dados na API USP Graduação.

## Descrição Técnica

A configuração do banco de dados é definida no arquivo `app/database.py`, que utiliza o SQLAlchemy para criar uma conexão com o PostgreSQL e gerenciar sessões de banco de dados.

### Configuração de Conexão

```python
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

# URL de conexão ao banco de dados padrão
TARGET_DATABASE = "api_db"
SCHEMA_NAME = "api"
DATABASE_URL = f"postgresql://postgres:1234@localhost/{TARGET_DATABASE}"

# Crie o engine com o schema padrão 'api'
engine = create_engine(DATABASE_URL, connect_args={"options": f"-csearch_path={SCHEMA_NAME}"})

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Componentes Principais

1. **DATABASE_URL**: String de conexão para o PostgreSQL que especifica host, usuário, senha e nome do banco de dados.
2. **engine**: Instância do SQLAlchemy Engine que estabelece conexões com o banco de dados.
3. **SessionLocal**: Factory de sessões do SQLAlchemy para criar sessões de banco de dados.
4. **get_db()**: Função que cria uma nova sessão de banco de dados para uso nos endpoints da API.

## Criação do Banco de Dados

O banco de dados e o schema são criados através do script `templates/create_db.py`:

```python
import psycopg2
from psycopg2 import sql

# Configurações do banco de dados
DATABASE_URL = "postgresql://postgres:1234@localhost/postgres"
TARGET_DATABASE = "api_db"
SCHEMA_NAME = "api"

# Função para criar o banco de dados se não existir
def create_database_if_not_exists():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [TARGET_DATABASE])
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(TARGET_DATABASE)))
        conn.commit()
    cursor.close()
    conn.close()

# Função para criar o schema se não existir
def create_schema_if_not_exists():
    conn = psycopg2.connect(f"postgresql://postgres:1234@localhost/{TARGET_DATABASE}")
    cursor = conn.cursor()
    cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(SCHEMA_NAME)))
    conn.commit()
    cursor.close()
    conn.close()

# Criar banco de dados e schema
create_database_if_not_exists()
create_schema_if_not_exists()
```

## Gerenciamento de Sessões

As sessões de banco de dados são criadas automaticamente para cada requisição da API através do sistema de dependências do FastAPI. A função `get_db()` é passada como uma dependência para os endpoints da API:

```python
@app.post("/registro/", response_model=schemas.Registro)
def create_registro(registro: schemas.RegistroCreate, db: Session = Depends(get_db)):
    # Implementação do endpoint
```

## Exemplos de Uso

### Conexão Direta ao Banco de Dados

```python
from app.database import engine, SessionLocal
from sqlalchemy import text

# Executando SQL direto com o engine
with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM api.registros"))
    for row in result:
        print(row)

# Usando uma sessão
db = SessionLocal()
try:
    result = db.execute(text("SELECT * FROM api.registros"))
    for row in result:
        print(row)
finally:
    db.close()
```

### Uso com FastAPI

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db

@app.get("/exemplo/")
def exemplo_endpoint(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT COUNT(*) FROM api.registros")).scalar()
    return {"total_registros": result}
```

## Configuração do Banco de Dados

Para configurar o banco de dados, siga estas etapas:

1. Certifique-se de que o PostgreSQL esteja instalado e em execução
2. Execute o script de criação do banco de dados:

```bash
python templates/create_db.py
```

3. Execute as migrações do Alembic para criar as tabelas:

```bash
alembic upgrade head
```

## Testes da Conexão

Para testar a conexão com o banco de dados, você pode usar o seguinte comando:

```python
from app.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print(result.scalar())  # Deve retornar 1
```