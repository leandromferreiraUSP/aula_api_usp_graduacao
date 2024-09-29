from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional


# Obtém um registro específico com base no id_
def get_registro(db: Session, id: int, area: Optional[str] = None):
    return db.query(models.Registro).filter(models.Registro.id == id).first()


# Obtém um registro específico com base no id_cidade e, opcionalmente, na área
def get_registro_cidade(db: Session, id_cidade: int, area: Optional[str] = None):
    if area:
        return db.query(models.Registro).filter(models.Registro.id_cidade == id_cidade, models.Registro.area == area).first()
    return db.query(models.Registro).filter(models.Registro.id_cidade == id_cidade).first()

# Obtém todos os registros
def get_registros(db: Session):
    return db.query(models.Registro).all()

# Cria um novo registro
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

# Deleta um registro com base no ID
def delete_registro(db: Session, id: int):
    registro = get_registro(db, id)
    if registro:
        db.delete(registro)
        db.commit()
    return registro

# Busca registros com base no número de visitados
def search_by_visitados(db: Session, min_visitados: int, max_visitados: int):
    return db.query(models.Registro).filter(models.Registro.visitados.between(min_visitados, max_visitados)).all()