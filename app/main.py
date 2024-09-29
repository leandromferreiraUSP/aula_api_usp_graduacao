from fastapi import HTTPException, Depends, status
from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
import app.schemas as schemas
import app.crud as crud
from app.database import get_db

app = FastAPI()

# Endpoint para inserir dados unitários
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

# Endpoint para inserir dados como lista
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

 
# Endpoint para buscar um registro por ID
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

# Endpoint para buscar registros com base no número de visitados
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
    
# Endpoint para buscar todos os registros
@app.get("/registros/", response_model=List[schemas.Registro])
def read_registros(db: Session = Depends(get_db)):
    try:
        return crud.get_registros(db=db)
    except HTTPException as e:
        raise e  
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

# Endpoint para buscar um registro por id_cidade e, opcionalmente, área
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


# Endpoint para deletar um registro por ID
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
    



