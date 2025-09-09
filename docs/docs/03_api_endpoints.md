# API Endpoints

Os endpoints da API são a interface principal para interação com o sistema. Eles permitem a criação, consulta e exclusão de registros através de requisições HTTP.

## Descrição Técnica

Os endpoints da API são implementados no arquivo `app/main.py` usando o framework FastAPI. Cada endpoint corresponde a uma rota HTTP específica e está associado a uma função que processa a requisição e retorna uma resposta.

### Configuração Básica da API

```python
from fastapi import FastAPI
from sqlalchemy.orm import Session
import app.schemas as schemas
import app.crud as crud
from app.database import get_db

app = FastAPI()

# Endpoints são definidos aqui
```

### Lista de Endpoints Disponíveis

| Método HTTP | Rota | Descrição | Parâmetros |
|-------------|------|-----------|------------|
| POST | `/registro/` | Criar um novo registro | Body: `RegistroCreate` |
| POST | `/registros/batch/` | Criar múltiplos registros | Body: `List[RegistroCreate]` |
| GET | `/registros/{id_registro}` | Buscar registro por ID | Path: `id_registro` |
| GET | `/registros/search/` | Buscar registros por visitados | Query: `min_visitados`, `max_visitados` |
| GET | `/registros/` | Listar todos os registros | Nenhum |
| GET | `/registros/cidade/{id_cidade}` | Buscar registros por cidade | Path: `id_cidade`, Query: `area` (opcional) |
| DELETE | `/registros/{id_registro}` | Excluir registro por ID | Path: `id_registro` |

## Implementação Detalhada dos Endpoints

### Criar Registro (POST `/registro/`)

```python
@app.post("/registro/", response_model=schemas.Registro)
def create_registro(registro: schemas.RegistroCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_registro(db=db, registro=registro)
    except HTTPException as e:
        raise e  
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Erro de chave primária: o ID já existe.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
```

### Criar Múltiplos Registros (POST `/registros/batch/`)

```python
@app.post("/registros/batch/", response_model=List[schemas.Registro])
def create_registros(registros: List[schemas.RegistroCreate], db: Session = Depends(get_db)):
    try:
        return [crud.create_registro(db=db, registro=registro) for registro in registros]
    except HTTPException as e:
        raise e  
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
```

### Buscar Registro por ID (GET `/registros/{id_registro}`)

```python
@app.get("/registros/{id_registro}", response_model=schemas.Registro)
def read_registro(id_registro: int, db: Session = Depends(get_db)):
    try:
        registro = crud.get_registro(db=db, id=id_registro)
        if registro is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro não encontrado")
        return registro
    except HTTPException as e:
        raise e 
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
```

### Buscar Registros por Visitados (GET `/registros/search/`)

```python
@app.get("/registros/search/", response_model=List[schemas.Registro])
def search_visitados(min_visitados: int, max_visitados: int, db: Session = Depends(get_db)):
    if min_visitados is None or max_visitados is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filtros min_visitados e max_visitados são obrigatórios")
    try:
        return crud.search_by_visitados(db=db, min_visitados=min_visitados, max_visitados=max_visitados)
    except HTTPException as e:
        raise e  
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
```

### Listar Todos os Registros (GET `/registros/`)

```python
@app.get("/registros/", response_model=List[schemas.Registro])
def read_registros(db: Session = Depends(get_db)):
    try:
        return crud.get_registros(db=db)
    except HTTPException as e:
        raise e  
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
```

### Buscar Registro por Cidade (GET `/registros/cidade/{id_cidade}`)

```python
@app.get("/registros/cidade/{id_cidade}", response_model=schemas.Registro)
def read_registro_cidade(id_cidade: int, area: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        registro = crud.get_registro_cidade(db=db, id_cidade=id_cidade, area=area)
        if registro is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro não encontrado")
        return registro
    except HTTPException as e:
        raise e  
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
```

### Excluir Registro (DELETE `/registros/{id_registro}`)

```python
@app.delete("/registros/{id_registro}", response_model=schemas.Registro)
def delete_registro(id_registro: int, db: Session = Depends(get_db)):
    try:
        registro = crud.delete_registro(db=db, id=id_registro)
        if registro is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro não encontrado")
        return registro
    except HTTPException as e:
        raise e  
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
```

## Tratamento de Erros

Os endpoints incluem tratamento de erros para diversas situações, como:

- Validação de dados de entrada (usando Pydantic)
- Erros de integridade do banco de dados (como chaves primárias duplicadas)
- Registros não encontrados
- Erros internos do servidor

Cada tipo de erro retorna um código de status HTTP apropriado e uma mensagem descritiva.

## Exemplos de Uso

### Criação de um Registro

```bash
curl -X POST "http://localhost:8000/registro/" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "id_cidade": 589,
    "nome": "SOROCABA",
    "area": "Norte",
    "imoveis": 29313,
    "trabalhados": 19,
    "nao_trabalhados": 23,
    "pend": 54.76,
    "visitados": 42
  }'
```

### Listagem de Todos os Registros

```bash
curl -X GET "http://localhost:8000/registros/"
```

### Busca de Registro por ID

```bash
curl -X GET "http://localhost:8000/registros/1"
```

### Exclusão de Registro

```bash
curl -X DELETE "http://localhost:8000/registros/1"
```