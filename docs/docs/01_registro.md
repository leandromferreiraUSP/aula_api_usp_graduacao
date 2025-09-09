# Registro

O Registro é a entidade principal da API USP Graduação, representando os dados de imóveis em diferentes áreas de cidades. Esta abstração é implementada tanto como um modelo SQLAlchemy quanto como um schema Pydantic.

## Descrição Técnica

O Registro é definido como uma tabela no banco de dados PostgreSQL através da classe `Registro` no arquivo `app/models.py`. A tabela é criada no esquema `api` do banco de dados.

### Modelo SQLAlchemy

```python
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
```

### Atributos do Registro

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `id` | Integer | Identificador único do registro (chave primária) |
| `id_cidade` | Integer | Identificador da cidade |
| `nome` | String | Nome da cidade |
| `area` | String | Área específica dentro da cidade |
| `imoveis` | Integer | Quantidade total de imóveis na área |
| `trabalhados` | Integer | Quantidade de imóveis já trabalhados |
| `nao_trabalhados` | Integer | Quantidade de imóveis não trabalhados |
| `pend` | Float | Percentual de pendência (cálculo: `nao_trabalhados / visitados * 100`) |
| `visitados` | Integer | Quantidade de imóveis visitados (soma de `trabalhados` e `nao_trabalhados`) |

## Schemas Pydantic

O Registro também é representado como um schema Pydantic no arquivo `app/schemas.py` para validação de dados e serialização/deserialização:

```python
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

### Classes de Schema

1. **RegistroBase**: Define os atributos básicos que todos os schemas de registro devem ter.
2. **RegistroCreate**: Utilizado para validar os dados ao criar um novo registro.
3. **Registro**: Utilizado para serializar dados ao retornar um registro existente.

## Exemplos de Uso

### Criando um Novo Registro

```python
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

# Serialização/Validação com Pydantic
registro = schemas.RegistroCreate(**registro_data)

# Criação no banco de dados
db_registro = models.Registro(**registro.dict())
db.add(db_registro)
db.commit()
db.refresh(db_registro)
```

### Recuperando um Registro

```python
# Busca por ID
registro = db.query(models.Registro).filter(models.Registro.id == 1).first()

# Conversão para dict/JSON
registro_dict = schemas.Registro.from_orm(registro).dict()
```

## Testando Operações com Registro

Para testar operações relacionadas ao modelo Registro, você pode utilizar os scripts localizados no diretório `requests_api/`. Por exemplo, para criar um novo registro:

```bash
python requests_api/create_registro.py
```

Este script envia uma requisição POST para a API com os dados de um novo registro e exibe o resultado.