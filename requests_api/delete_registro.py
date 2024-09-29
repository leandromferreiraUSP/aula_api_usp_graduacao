import requests

# ID e área do registro a ser deletado
registro_id = 11

# URL do endpoint
url = f"http://127.0.0.1:8000/registros/{registro_id}"

# Fazer a requisição DELETE para excluir um registro
response = requests.delete(url)

# Mostrar o resultado
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")