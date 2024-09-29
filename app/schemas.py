from pydantic import BaseModel
from typing import List, Optional 

class RegistroBase(BaseModel):
    id: int
    id_cidade: int
    nome: str
    area: str
    imoveis: int
    trabalhados: int
    nao_trabalhados: int
    pend: float
    visitados: int

class RegistroCreate(RegistroBase):
    pass

class Registro(RegistroBase):
    id: int

    class Config:
        orm_mode = True
