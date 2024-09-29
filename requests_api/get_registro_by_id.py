import requests

# ID e área do registro a ser buscado
registro_id = 2

# URL do endpoint
url = f"http://127.0.0.1:8000/registros/{registro_id}"

# Fazer a requisição GET para buscar um registro específico
response = requests.get(url)

# Mostrar o resultado
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")