# Operações CRUD

As operações CRUD (Create, Read, Update, Delete) formam a camada de acesso a dados da API USP Graduação. Esta abstração encapsula todas as interações diretas com o banco de dados, fornecendo funções de alto nível para os endpoints da API.

## Descrição Técnica

As operações CRUD são implementadas no arquivo `app/crud.py` e fornecem métodos para criar, ler, buscar e excluir registros no banco de dados. Estas funções são utilizadas pelos endpoints da API definidos em `app/main.py`.

### Importações e Dependências

```python
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
```

## Funções Disponíveis

### Buscar Registro por ID

```python
def get_registro(db: Session, id: int, area: Optional[str] = None):
    return db.query(models.Registro).filter(models.Registro.id == id).first()
```

**Parâmetros:**
- `db`: Sessão do SQLAlchemy para interagir com o banco de dados
- `id`: ID do registro a ser buscado
- `area`: (Não utilizado nesta função, mas mantido para compatibilidade)

**Retorno:**
- Instância do modelo `Registro` ou `None` se não encontrado

### Buscar Registro por Cidade e Área

```python
def get_registro_cidade(db: Session, id_cidade: int, area: Optional[str] = None):
    if area:
        return db.query(models.Registro).filter(models.Registro.id_cidade == id_cidade, models.Registro.area == area).first()
    return db.query(models.Registro).filter(models.Registro.id_cidade == id_cidade).first()
```

**Parâmetros:**
- `db`: Sessão do SQLAlchemy
- `id_cidade`: ID da cidade a ser buscada
- `area`: (Opcional) Área específica dentro da cidade

**Retorno:**
- Instância do modelo `Registro` ou `None` se não encontrado

### Listar Todos os Registros

```python
def get_registros(db: Session):
    return db.query(models.Registro).all()
```

**Parâmetros:**
- `db`: Sessão do SQLAlchemy

**Retorno:**
- Lista de instâncias do modelo `Registro`

### Criar Novo Registro

```python
def create_registro(db: Session, registro: schemas.RegistroCreate):
    try:
        db_registro = models.Registro(
            id=registro.id,
            id_cidade=registro.id_cidade,
            nome=registro.nome,
            area=registro.area,
            imoveis=registro.imoveis,
            trabalhados=registro.trabalhados,
            nao_trabalhados=registro.nao_trabalhados,
            pend=registro.pend,
            visitados=registro.visitados
        )
        db.add(db_registro)
        db.commit()
        db.refresh(db_registro)
        return db_registro
    except SQLAlchemyError as e:
        db.rollback()
        raise e
```

**Parâmetros:**
- `db`: Sessão do SQLAlchemy
- `registro`: Instância do schema `RegistroCreate` com os dados do novo registro

**Retorno:**
- Instância do modelo `Registro` criado

**Exceções:**
- `SQLAlchemyError`: Em caso de erros de banco de dados (ex: violação de chave única)

### Excluir Registro

```python
def delete_registro(db: Session, id: int):
    registro = get_registro(db, id)
    if registro:
        db.delete(registro)
        db.commit()
    return registro
```

**Parâmetros:**
- `db`: Sessão do SQLAlchemy
- `id`: ID do registro a ser excluído

**Retorno:**
- Instância do modelo `Registro` excluído, ou `None` se não encontrado

### Buscar Registros por Faixa de Visitados

```python
def search_by_visitados(db: Session, min_visitados: int, max_visitados: int):
    return db.query(models.Registro).filter(models.Registro.visitados.between(min_visitados, max_visitados)).all()
```

**Parâmetros:**
- `db`: Sessão do SQLAlchemy
- `min_visitados`: Valor mínimo do campo `visitados`
- `max_visitados`: Valor máximo do campo `visitados`

**Retorno:**
- Lista de instâncias do modelo `Registro` que atendem aos critérios

## Exemplos de Uso

### Criação de um Registro

```python
from app.database import SessionLocal
import app.schemas as schemas
import app.crud as crud

# Dados do registro
registro_data = {
    "id": 1,
    "id_cidade": 589,
    "nome": "SOROCABA",
    "area": "Norte",
    "imoveis": 29313,
    "trabalhados": 19,
    "nao_trabalhados": 23,
    "pend": 54.76,
    "visitados": 42
}

# Criação do schema
registro_schema = schemas.RegistroCreate(**registro_data)

# Criação no banco de dados
db = SessionLocal()
try:
    novo_registro = crud.create_registro(db, registro_schema)
    print(f"Registro criado com ID: {novo_registro.id}")
finally:
    db.close()
```

### Busca de Registros

```python
from app.database import SessionLocal
import app.crud as crud

db = SessionLocal()
try:
    # Buscar por ID
    registro = crud.get_registro(db, id=1)
    if registro:
        print(f"Registro encontrado: {registro.nome}, Área: {registro.area}")
    
    # Buscar por cidade e área
    registro_cidade = crud.get_registro_cidade(db, id_cidade=589, area="Norte")
    if registro_cidade:
        print(f"Registro por cidade: {registro_cidade.nome}, Área: {registro_cidade.area}")
    
    # Listar todos
    registros = crud.get_registros(db)
    print(f"Total de registros: {len(registros)}")
    
    # Buscar por visitados
    registros_visitados = crud.search_by_visitados(db, min_visitados=30, max_visitados=100)
    print(f"Registros por visitados: {len(registros_visitados)}")
finally:
    db.close()
```

### Exclusão de Registro

```python
from app.database import SessionLocal
import app.crud as crud

db = SessionLocal()
try:
    # Excluir registro
    registro_excluido = crud.delete_registro(db, id=1)
    if registro_excluido:
        print(f"Registro excluído: {registro_excluido.id}")
    else:
        print("Registro não encontrado")
finally:
    db.close()
```

## Testes de Operações CRUD

Os scripts no diretório `requests_api/` podem ser utilizados para testar as operações CRUD através da API:

- `create_registro.py` - Testa a criação de um registro
- `create_registro_batch.py` - Testa a criação de múltiplos registros
- `get_registro_by_id.py` - Testa a busca por ID
- `get_registro_cidade.py` - Testa a busca por cidade e área
- `get_registros.py` - Testa a listagem de todos os registros
- `search_by_visitados.py` - Testa a busca por faixa de visitados
- `delete_registro.py` - Testa a exclusão de um registro