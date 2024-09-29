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