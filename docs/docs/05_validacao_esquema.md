# Validação de Esquema

A validação de esquema é uma abstração crucial na API USP Graduação, responsável por garantir que os dados recebidos e enviados pela API estejam em conformidade com as estruturas esperadas. Esta validação é implementada usando a biblioteca Pydantic.

## Descrição Técnica

Os esquemas de validação são definidos no arquivo `app/schemas.py` usando as classes do Pydantic. Esses esquemas definem a estrutura dos objetos de dados e realizam validações automáticas.

### Esquemas Básicos

```python
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
```

## Estrutura dos Esquemas

1. **RegistroBase**

   Classe base que define todos os campos necessários para um registro.

   **Campos:**
   
   - `id`: Identificador único (inteiro)
   - `id_cidade`: Identificador da cidade (inteiro)
   - `nome`: Nome da cidade (string)
   - `area`: Área dentro da cidade (string)
   - `imoveis`: Número total de imóveis (inteiro)
   - `trabalhados`: Número de imóveis trabalhados (inteiro)
   - `nao_trabalhados`: Número de imóveis não trabalhados (inteiro)
   - `pend`: Percentual de pendência (float)
   - `visitados`: Número de imóveis visitados (inteiro)

2. **RegistroCreate**

   Esquema usado para validar dados ao criar um novo registro. Herda todos os campos de `RegistroBase`.

3. **Registro**

   Esquema usado para retornar dados de registros existentes. Herda todos os campos de `RegistroBase` e adiciona configuração para converter objetos ORM em resposta JSON.

   **Configuração:**
   
   - `orm_mode = True`: Permite que o Pydantic converta objetos SQLAlchemy em dicionários/JSON.

## Funcionamento da Validação

Quando uma requisição é recebida pela API, o FastAPI automaticamente usa o Pydantic para validar os dados de entrada:

1. Os dados JSON da requisição são convertidos em uma instância do esquema Pydantic.
2. Durante essa conversão, o Pydantic valida os tipos de dados e formatos conforme definido no esquema.
3. Se os dados forem inválidos, o FastAPI retorna automaticamente um erro HTTP 422 com detalhes sobre as falhas de validação.
4. Se os dados forem válidos, a instância do esquema é passada para a função do endpoint.

## Exemplos de Uso

### Validação de Dados de Entrada

```python
from app.schemas import RegistroCreate
from fastapi import HTTPException

# Dados de entrada do cliente
dados_json = {
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

# Validação do Pydantic (ocorre automaticamente no FastAPI)
try:
    registro = RegistroCreate(**dados_json)
    print("Dados válidos:", registro)
except Exception as e:
    # Isso seria automaticamente capturado pelo FastAPI
    raise HTTPException(status_code=422, detail=str(e))
```

### Conversão de Objeto ORM para Resposta

```python
from app.models import Registro as RegistroModel
from app.schemas import Registro as RegistroSchema

# Suponha que temos um objeto do SQLAlchemy
registro_orm = db.query(RegistroModel).first()

# Conversão para o formato de resposta
# No FastAPI isso é feito automaticamente ao especificar response_model
registro_resposta = RegistroSchema.from_orm(registro_orm)
resposta_json = registro_resposta.dict()
```

### Exemplo de Validação em um Endpoint

```python
@app.post("/registro/", response_model=schemas.Registro)
def create_registro(registro: schemas.RegistroCreate, db: Session = Depends(get_db)):
    # A este ponto, 'registro' já foi validado pelo Pydantic
    # Se os dados fossem inválidos, uma exceção teria sido lançada antes de chegar aqui
    
    # Podemos usar os dados com segurança
    return crud.create_registro(db=db, registro=registro)
```

## Personalização de Validações

O Pydantic permite personalizar as validações usando validadores e configurações adicionais:

```python
from pydantic import BaseModel, validator

class RegistroComValidacao(BaseModel):
    id: int
    id_cidade: int
    nome: str
    area: str
    imoveis: int
    trabalhados: int
    nao_trabalhados: int
    pend: float
    visitados: int
    
    @validator('imoveis', 'trabalhados', 'nao_trabalhados', 'visitados')
    def validar_numeros_positivos(cls, v, values, **kwargs):
        if v < 0:
            raise ValueError(f'O valor deve ser positivo')
        return v
    
    @validator('visitados')
    def validar_visitados(cls, v, values, **kwargs):
        trabalhados = values.get('trabalhados', 0)
        nao_trabalhados = values.get('nao_trabalhados', 0)
        if v != trabalhados + nao_trabalhados:
            raise ValueError('visitados deve ser igual a trabalhados + nao_trabalhados')
        return v
```

## Atualizando para Pydantic V2

A API atual está usando uma versão do Pydantic que usa `orm_mode`, que foi substituído por `from_attributes` na V2. A atualização seria:

```python
class Registro(RegistroBase):
    id: int

    class Config:
        from_attributes = True  # Substitui orm_mode = True
```

## Testando Validações

Para testar a validação de esquemas, você pode criar um script Python simples:

```python
from app.schemas import RegistroCreate

# Teste com dados válidos
dados_validos = {
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

# Teste com dados inválidos
dados_invalidos = {
    "id": "não é um número",  # Deveria ser um inteiro
    "id_cidade": 589,
    "nome": "SOROCABA",
    "area": "Norte",
    "imoveis": 29313,
    "trabalhados": 19,
    "nao_trabalhados": 23,
    "pend": 54.76,
    "visitados": 42
}

try:
    registro_valido = RegistroCreate(**dados_validos)
    print("Validação bem-sucedida:", registro_valido)
except Exception as e:
    print("Erro de validação:", e)

try:
    registro_invalido = RegistroCreate(**dados_invalidos)
    print("Validação bem-sucedida (não deveria acontecer):", registro_invalido)
except Exception as e:
    print("Erro de validação esperado:", e)
```