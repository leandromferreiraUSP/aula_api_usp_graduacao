# Criando Registros

Neste tutorial, aprenderemos como criar novos registros usando a API USP Graduação.

## Pré-requisitos

Antes de começar, certifique-se de que:

- A API está em execução (como explicado em [Iniciando a API](03_iniciando_api.md))
- O banco de dados PostgreSQL está funcionando
- As migrações do Alembic foram aplicadas

## Entendendo o modelo de dados

Para criar um registro corretamente, é importante entender sua estrutura. Na API USP Graduação, um registro contém as seguintes informações:

| Campo | Tipo | Descrição | Obrigatório |
|-------|------|-----------|-------------|
| id_cidade | Integer | Identificador único da cidade | Sim |
| nome | String | Nome do registro/localidade | Sim |
| area | Float | Área em km² | Sim |
| imoveis | Integer | Número de imóveis na região | Sim |
| populacao | Integer | População estimada | Sim |
| visitados | Boolean | Se a região já foi visitada | Sim |
| descricao | String | Descrição detalhada | Não |

## Passo 1: Criar um registro usando a interface Swagger

A maneira mais fácil para começar é utilizar a documentação interativa:

1. Abra o navegador e acesse [http://localhost:8000/docs](http://localhost:8000/docs)
2. Localize e clique no endpoint `POST /registros/`
3. Clique em "Try it out"
4. No editor de JSON, insira os dados do registro seguindo este modelo:

```json
{
  "id_cidade": 1,
  "nome": "Vila Madalena",
  "area": 2.5,
  "imoveis": 3200,
  "populacao": 15000,
  "visitados": true,
  "descricao": "Bairro residencial com muitos bares e restaurantes"
}
```

5. Clique em "Execute"
6. Observe a resposta. Se for bem-sucedida, você verá o registro criado com um `id` gerado pelo sistema

## Passo 2: Criar um registro usando Python

Para automatizar o processo de criação, você pode usar o script Python fornecido no projeto. Vamos analisar o arquivo `requests_api/create_registro.py`:

```python
import requests
import json

# URL da API
url = "http://localhost:8000/registros/"

# Dados do novo registro
novo_registro = {
    "id_cidade": 2,
    "nome": "Pinheiros",
    "area": 3.7,
    "imoveis": 4800,
    "populacao": 28000,
    "visitados": True,
    "descricao": "Bairro comercial e residencial"
}

# Enviando a requisição POST
response = requests.post(url, json=novo_registro)

# Verificando a resposta
if response.status_code == 200:
    print("Registro criado com sucesso!")
    print(json.dumps(response.json(), indent=4))
else:
    print(f"Erro: {response.status_code}")
    print(response.text)
```

Para executar este script:

```bash
# Certifique-se de que o ambiente virtual está ativado
python requests_api/create_registro.py
```

## Passo 3: Criar múltiplos registros de uma vez

Se você precisar criar vários registros simultaneamente, pode usar o endpoint de criação em lote ou adaptar o script Python:

### Usando o endpoint de batch

1. Acesse [http://localhost:8000/docs](http://localhost:8000/docs)
2. Localize e clique no endpoint `POST /registros/batch/`
3. Clique em "Try it out"
4. No editor JSON, insira um array de registros:

```json
[
  {
    "id_cidade": 3,
    "nome": "Moema",
    "area": 4.2,
    "imoveis": 5600,
    "populacao": 31000,
    "visitados": true,
    "descricao": "Bairro residencial de alto padrão"
  },
  {
    "id_cidade": 4,
    "nome": "Vila Mariana",
    "area": 3.1,
    "imoveis": 4200,
    "populacao": 25000,
    "visitados": false,
    "descricao": "Bairro com muitas escolas e faculdades"
  }
]
```

5. Clique em "Execute"
6. Observe a resposta com os registros criados

### Usando o script para criação em lote

Você também pode usar o script `requests_api/create_registro_batch.py`:

```python
import requests
import json

# URL da API para criação em lote
url = "http://localhost:8000/registros/batch/"

# Lista de registros para criar
registros = [
    {
        "id_cidade": 5,
        "nome": "Itaim Bibi",
        "area": 2.8,
        "imoveis": 4100,
        "populacao": 22000,
        "visitados": True,
        "descricao": "Bairro empresarial com muitos escritórios"
    },
    {
        "id_cidade": 6,
        "nome": "Jardins",
        "area": 3.5,
        "imoveis": 3900,
        "populacao": 18500,
        "visitados": True,
        "descricao": "Bairro residencial de alto padrão com muito comércio"
    }
]

# Enviando a requisição POST
response = requests.post(url, json=registros)

# Verificando a resposta
if response.status_code == 200:
    print("Registros criados com sucesso!")
    print(json.dumps(response.json(), indent=4))
else:
    print(f"Erro: {response.status_code}")
    print(response.text)
```

Execute o script:

```bash
python requests_api/create_registro_batch.py
```

## Validação e tratamento de erros

A API implementa validação de dados usando Pydantic. Se você enviar dados inválidos, receberá uma resposta de erro clara. Alguns exemplos comuns:

- **Valores incorretos**: Se enviar tipos de dados incorretos (texto em campos numéricos)
- **Campos obrigatórios ausentes**: Se omitir campos marcados como obrigatórios
- **Valores fora de limites**: Se enviar valores que não respeitam as restrições (ex: área negativa)

Quando ocorrer um erro de validação, a API retornará um código de status HTTP 422 e detalhes sobre o erro.

## Próximos passos

Agora que você já sabe como criar registros, aprenda como:

- [Consultando Registros](05_consultando_registros.md) - Como buscar os registros que você criou.