from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Registro(Base):
    __tablename__ = "registros"
    __table_args__ = {'schema': 'api'}

    id = Column(Integer, primary_key=True, index=True)
    id_cidade = Column(Integer, index=True)
    nome = Column(String, index=True)
    area = Column(String, index=True)
    imoveis = Column(Integer)
    trabalhados = Column(Integer)
    nao_trabalhados = Column(Integer)
    pend = Column(Float)
    visitados = Column(Integer)