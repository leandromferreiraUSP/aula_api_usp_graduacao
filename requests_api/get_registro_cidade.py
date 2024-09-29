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

# Exemplos de uso:
# print(get_registro_por_cidade(589))

print("\n\n\n\n")


print(get_registro_por_cidade_e_area(589, "Norte"))