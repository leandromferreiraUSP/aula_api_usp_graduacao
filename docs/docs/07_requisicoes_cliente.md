# Requisições de Cliente

As Requisições de Cliente representam a camada que interage com a API, enviando solicitações HTTP e processando respostas. Na API USP Graduação, esta abstração é implementada através de um conjunto de scripts Python que demonstram como utilizar cada endpoint da API.

## Descrição Técnica

Os scripts de cliente estão localizados no diretório `requests_api/` e são implementados usando a biblioteca `requests` do Python. Cada script demonstra uma operação específica da API, como criar, buscar ou excluir registros.

### Importações Comuns

```python
import requests
```

## Scripts Disponíveis

### 1. Criação de Registro Individual (`create_registro.py`)

```python
import requests

# URL do endpoint
url = "http://127.0.0.1:8000/registro/"

# Dados do registro
registro_data = {
    "id": -1,
    "id_cidade": 589,
    "nome": "SOROCABA",
    "area": "TESTE",
    "imoveis": -1,
    "trabalhados": 999,  
    "nao_trabalhados": 999, 
    "pend": 99.9,  
    "visitados": 99  
}

# Fazer a requisição POST para criar um registro
response = requests.post(url, json=registro_data)

# Mostrar o resultado
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
```

### 2. Criação de Múltiplos Registros (`create_registro_batch.py`)

```python
import requests

# URL do endpoint
url = "http://127.0.0.1:8000/registros/batch/"

# Dados de vários registros
registros_data = [
    {
        "id": 11,
        "id_cidade": 589,
        "nome": "SOROCABA",
        "area": "Norte",
        "imoveis": 29313,
        "trabalhados": 19,
        "nao_trabalhados": 23,
        "pend": 54.76,
        "visitados": 42
    },
    # ... outros registros ...
]

# Fazer a requisição POST para criar vários registros
response = requests.post(url, json=registros_data)

# Mostrar o resultado
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
```

### 3. Busca de Registro por ID (`get_registro_by_id.py`)

```python
import requests

# ID do registro a ser buscado
registro_id = 2

# URL do endpoint
url = f"http://127.0.0.1:8000/registros/{registro_id}"

# Fazer a requisição GET para buscar um registro específico
response = requests.get(url)

# Mostrar o resultado
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
```

### 4. Busca de Registro por Cidade (`get_registro_cidade.py`)

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

def get_registro_por_cidade(id_cidade: int):
    url = f"{BASE_URL}/registros/cidade/{id_cidade}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao buscar registro: {response.status_code} - {response.text}")

def get_registro_por_cidade_e_area(id_cidade: int, area: str):
    url = f"{BASE_URL}/registros/cidade/{id_cidade}"
    params = {"area": area}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao buscar registro: {response.status_code} - {response.text}")

# Exemplo de uso
print(get_registro_por_cidade_e_area(589, "Norte"))
```

### 5. Listagem de Todos os Registros (`get_registros.py`)

```python
import requests

# URL do endpoint
url = "http://127.0.0.1:8000/registros/"

# Fazer a requisição GET para buscar todos os registros
response = requests.get(url)

# Mostrar o resultado
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
```

### 6. Busca por Faixa de Visitados (`search_by_visitados.py`)

```python
import requests

# Parâmetros para a busca
min_visitados = 30
max_visitados = 50

# URL do endpoint
url = f"http://127.0.0.1:8000/registros/search/?min_visitados={min_visitados}&max_visitados={max_visitados}"

# Fazer a requisição GET para buscar registros com base no número de visitados
response = requests.get(url)

# Mostrar o resultado
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
```

### 7. Exclusão de Registro (`delete_registro.py`)

```python
import requests

# ID do registro a ser deletado
registro_id = 11

# URL do endpoint
url = f"http://127.0.0.1:8000/registros/{registro_id}"

# Fazer a requisição DELETE para excluir um registro
response = requests.delete(url)

# Mostrar o resultado
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
```

## Como Utilizar os Scripts

Cada script pode ser executado diretamente com Python:

```bash
# Exemplo de execução do script de criação de registro
python requests_api/create_registro.py

# Exemplo de execução do script de listagem de registros
python requests_api/get_registros.py
```

## Personalização dos Scripts

Os scripts podem ser facilmente personalizados alterando os dados ou parâmetros:

1. **Modificar Dados de Registro**: Altere o dicionário `registro_data` ou a lista `registros_data`
2. **Modificar IDs de Busca**: Altere as variáveis `registro_id` ou `id_cidade`
3. **Modificar Parâmetros de Busca**: Altere as variáveis `min_visitados` e `max_visitados`

## Exemplos de Personalização

### Exemplo 1: Modificar Dados para Criação de Registro

```python
# Em create_registro.py
registro_data = {
    "id": 100,  # ID modificado
    "id_cidade": 123,  # Cidade modificada
    "nome": "CAMPINAS",  # Nome modificado
    "area": "Centro",  # Área modificada
    "imoveis": 5000,
    "trabalhados": 2500,
    "nao_trabalhados": 2500,
    "pend": 50.0,
    "visitados": 5000
}
```

### Exemplo 2: Modificar Parâmetros de Busca

```python
# Em search_by_visitados.py
min_visitados = 100  # Valor mínimo modificado
max_visitados = 1000  # Valor máximo modificado
```

## Tratamento de Erros

Os scripts demonstram tratamento básico de erros, mostrando o código de status e a resposta da API. Para scripts mais robustos, você pode implementar tratamento de erros mais detalhado:

```python
import requests

def fazer_requisicao_segura(url, metodo="GET", dados=None, params=None):
    try:
        if metodo.upper() == "GET":
            response = requests.get(url, params=params)
        elif metodo.upper() == "POST":
            response = requests.post(url, json=dados)
        elif metodo.upper() == "DELETE":
            response = requests.delete(url)
        else:
            raise ValueError(f"Método HTTP não suportado: {metodo}")
        
        response.raise_for_status()  # Levanta exceção para códigos de erro HTTP
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP: {e}")
        if response.text:
            print(f"Detalhes: {response.text}")
        return None
    except requests.exceptions.ConnectionError:
        print("Erro de conexão. Verifique se a API está em execução.")
        return None
    except requests.exceptions.Timeout:
        print("A requisição excedeu o tempo limite.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer requisição: {e}")
        return None
```

## Testes das Requisições

Para testar as requisições ao cliente, certifique-se de que:

1. A API esteja em execução (`python run_api.py`)
2. O banco de dados PostgreSQL esteja configurado e acessível
3. As migrações do Alembic tenham sido aplicadas (`alembic upgrade head`)

Depois, execute os scripts conforme necessário para testar as diferentes funcionalidades da API.