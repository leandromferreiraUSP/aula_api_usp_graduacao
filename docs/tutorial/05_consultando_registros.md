# Consultando Registros

Neste tutorial, aprenderemos como buscar e consultar registros usando a API USP Graduação.

## Pré-requisitos

Antes de começar, certifique-se de que:

- A API está em execução (como explicado em [Iniciando a API](03_iniciando_api.md))
- Existem registros no banco de dados (como explicado em [Criando Registros](04_criando_registros.md))

## Métodos de consulta disponíveis

A API USP Graduação oferece diversos métodos para consultar registros:

1. **Listar todos os registros**: Obtém uma lista completa de todos os registros
2. **Buscar por ID**: Localiza um registro específico pelo seu ID
3. **Buscar por cidade**: Filtra registros por ID da cidade
4. **Buscar por status de visitados**: Filtra registros por status de visitados (true/false)

Vamos explorar cada um desses métodos.

## Passo 1: Listar todos os registros

### Usando a interface Swagger

1. Abra o navegador e acesse [http://localhost:8000/docs](http://localhost:8000/docs)
2. Localize e clique no endpoint `GET /registros/`
3. Clique em "Try it out"
4. Clique em "Execute"
5. Observe a resposta: você verá uma lista de todos os registros cadastrados

### Usando Python

Você pode usar o script `requests_api/get_registros.py` para listar todos os registros:

```python
import requests
import json

# URL da API
url = "http://localhost:8000/registros/"

# Enviando a requisição GET
response = requests.get(url)

# Verificando a resposta
if response.status_code == 200:
    registros = response.json()
    print(f"Total de registros: {len(registros)}")
    print(json.dumps(registros, indent=4))
else:
    print(f"Erro: {response.status_code}")
    print(response.text)
```

Para executar o script:

```bash
# Certifique-se de que o ambiente virtual está ativado
python requests_api/get_registros.py
```

## Passo 2: Buscar registro por ID

Cada registro tem um identificador único (ID). Você pode buscar um registro específico usando este ID.

### Usando a interface Swagger

1. Abra o navegador e acesse [http://localhost:8000/docs](http://localhost:8000/docs)
2. Localize e clique no endpoint `GET /registros/{registro_id}`
3. Clique em "Try it out"
4. No campo `registro_id`, insira o ID do registro que você deseja consultar (por exemplo, 1)
5. Clique em "Execute"
6. Observe a resposta: você verá os detalhes do registro especificado

### Usando Python

Você pode usar o script `requests_api/get_registro_by_id.py` para buscar um registro por ID:

```python
import requests
import json
import sys

# Verificar se foi fornecido um ID como argumento
if len(sys.argv) < 2:
    print("Por favor, forneça o ID do registro como argumento.")
    print("Exemplo: python get_registro_by_id.py 1")
    sys.exit(1)

# Obter o ID do argumento da linha de comando
registro_id = sys.argv[1]

# URL da API com o ID específico
url = f"http://localhost:8000/registros/{registro_id}"

# Enviando a requisição GET
response = requests.get(url)

# Verificando a resposta
if response.status_code == 200:
    registro = response.json()
    print("Registro encontrado:")
    print(json.dumps(registro, indent=4))
elif response.status_code == 404:
    print(f"Registro com ID {registro_id} não encontrado.")
else:
    print(f"Erro: {response.status_code}")
    print(response.text)
```

Para executar o script:

```bash
python requests_api/get_registro_by_id.py 1
```

Substitua `1` pelo ID do registro que você deseja consultar.

## Passo 3: Buscar registros por cidade

Você pode filtrar registros com base no ID da cidade.

### Usando a interface Swagger

1. Abra o navegador e acesse [http://localhost:8000/docs](http://localhost:8000/docs)
2. Localize e clique no endpoint `GET /registros/cidade/{cidade_id}`
3. Clique em "Try it out"
4. No campo `cidade_id`, insira o ID da cidade que você deseja filtrar (por exemplo, 1)
5. Clique em "Execute"
6. Observe a resposta: você verá todos os registros associados a essa cidade

### Usando Python

Você pode usar o script `requests_api/get_registro_cidade.py` para buscar registros por cidade:

```python
import requests
import json
import sys

# Verificar se foi fornecido um ID como argumento
if len(sys.argv) < 2:
    print("Por favor, forneça o ID da cidade como argumento.")
    print("Exemplo: python get_registro_cidade.py 1")
    sys.exit(1)

# Obter o ID da cidade do argumento da linha de comando
cidade_id = sys.argv[1]

# URL da API com o ID da cidade
url = f"http://localhost:8000/registros/cidade/{cidade_id}"

# Enviando a requisição GET
response = requests.get(url)

# Verificando a resposta
if response.status_code == 200:
    registros = response.json()
    print(f"Total de registros encontrados para cidade {cidade_id}: {len(registros)}")
    print(json.dumps(registros, indent=4))
elif response.status_code == 404:
    print(f"Nenhum registro encontrado para cidade com ID {cidade_id}.")
else:
    print(f"Erro: {response.status_code}")
    print(response.text)
```

Para executar o script:

```bash
python requests_api/get_registro_cidade.py 1
```

Substitua `1` pelo ID da cidade que você deseja filtrar.

## Passo 4: Buscar por status de visitados

Você pode filtrar registros com base no status de visitados (true ou false).

### Usando a interface Swagger

1. Abra o navegador e acesse [http://localhost:8000/docs](http://localhost:8000/docs)
2. Localize e clique no endpoint `GET /registros/search/`
3. Clique em "Try it out"
4. No campo `visitados`, selecione `true` ou `false` conforme desejado
5. Clique em "Execute"
6. Observe a resposta: você verá todos os registros que correspondem ao status de visitados especificado

### Usando Python

Você pode usar o script `requests_api/search_by_visitados.py` para filtrar registros por status de visitados:

```python
import requests
import json
import sys

# Verificar se foi fornecido um valor de visitados como argumento
if len(sys.argv) < 2:
    print("Por favor, forneça o valor de visitados como argumento (true/false).")
    print("Exemplo: python search_by_visitados.py true")
    sys.exit(1)

# Obter o valor de visitados do argumento da linha de comando
visitados_input = sys.argv[1].lower()
if visitados_input == "true":
    visitados = True
elif visitados_input == "false":
    visitados = False
else:
    print("Valor inválido. Use 'true' ou 'false'.")
    sys.exit(1)

# URL da API com o parâmetro de consulta
url = f"http://localhost:8000/registros/search/?visitados={str(visitados).lower()}"

# Enviando a requisição GET
response = requests.get(url)

# Verificando a resposta
if response.status_code == 200:
    registros = response.json()
    print(f"Total de registros encontrados com visitados={visitados}: {len(registros)}")
    print(json.dumps(registros, indent=4))
else:
    print(f"Erro: {response.status_code}")
    print(response.text)
```

Para executar o script:

```bash
python requests_api/search_by_visitados.py true
```

Substitua `true` por `false` para buscar registros não visitados.

## Dicas para consultas eficientes

- **Filtragem do lado do servidor**: Sempre use os endpoints de filtragem disponíveis em vez de buscar todos os registros e filtrar no cliente
- **Verifique os códigos de erro**: Preste atenção aos códigos de status HTTP para diagnosticar problemas
- **Use IDs precisos**: Ao buscar por ID, certifique-se de usar o ID correto para evitar resultados vazios

## Próximos passos

Agora que você aprendeu como consultar registros, pode avançar para:

- [Atualizando Registros](06_atualizando_registros.md) - Como modificar registros existentes na API