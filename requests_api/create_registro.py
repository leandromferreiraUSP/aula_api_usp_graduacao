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