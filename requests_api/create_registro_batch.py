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
    {
        "id": 2,
        "id_cidade": 589,
        "nome": "SOROCABA",
        "area": "Centro Norte",
        "imoveis": 25604,
        "trabalhados": 19,
        "nao_trabalhados": 18,
        "pend": 48.65,
        "visitados": 37
    },
    {
        "id": 3,
        "id_cidade": 589,
        "nome": "SOROCABA",
        "area": "Centro Sul",
        "imoveis": 39207,
        "trabalhados": 5,
        "nao_trabalhados": 0,
        "pend": 0.00,
        "visitados": 5
    },
    {
        "id": 4,
        "id_cidade": 589,
        "nome": "SOROCABA",
        "area": "Leste",
        "imoveis": 30207,
        "trabalhados": 40,
        "nao_trabalhados": 43,
        "pend": 51.81,
        "visitados": 83
    },
    {
        "id": 5,
        "id_cidade": 589,
        "nome": "SOROCABA",
        "area": "Noroeste",
        "imoveis": 38170,
        "trabalhados": 117142,
        "nao_trabalhados": 27,
        "pend": 0.02,
        "visitados": 117169
    },
    {
        "id": 6,
        "id_cidade": 589,
        "nome": "SOROCABA",
        "area": "Sudoeste",
        "imoveis": 55319,
        "trabalhados": 6,
        "nao_trabalhados": 15,
        "pend": 71.43,
        "visitados": 21
    }
]

# Fazer a requisição POST para criar vários registros
response = requests.post(url, json=registros_data)

# Mostrar o resultado
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")