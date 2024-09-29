import requests

# URL do endpoint
url = "http://127.0.0.1:8000/registros/"

# Fazer a requisição GET para buscar todos os registros
response = requests.get(url)

# Mostrar o resultado
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
