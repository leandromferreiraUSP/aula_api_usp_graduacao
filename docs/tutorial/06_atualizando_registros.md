# Atualizando Registros

Neste tutorial, aprenderemos como atualizar registros existentes na API USP Graduação.

## Pré-requisitos

Antes de começar, certifique-se de que:

- A API está em execução (como explicado em [Iniciando a API](03_iniciando_api.md))
- Existem registros no banco de dados (como explicado em [Criando Registros](04_criando_registros.md))
- Você sabe como consultar registros (como explicado em [Consultando Registros](05_consultando_registros.md))

## Entendendo a atualização de registros

Na API USP Graduação, você pode atualizar um registro existente usando o método PUT. A atualização requer:

1. O ID do registro que deseja atualizar
2. Os novos dados que deseja aplicar ao registro

É importante notar que, com o método PUT, você precisa fornecer todos os campos do registro, mesmo aqueles que não deseja alterar. Para atualizações parciais, você precisaria implementar o método PATCH (não disponível nesta versão da API).

## Passo 1: Identificar o registro a ser atualizado

Primeiro, você precisa saber o ID do registro que deseja atualizar. Use um dos métodos de consulta vistos anteriormente:

```bash
# Listar todos os registros para encontrar o ID
python requests_api/get_registros.py

# Ou buscar um registro específico se já souber o ID
python requests_api/get_registro_by_id.py 1
```

Anote o ID e os dados atuais do registro que deseja modificar.

## Passo 2: Atualizar o registro usando a interface Swagger

1. Abra o navegador e acesse [http://localhost:8000/docs](http://localhost:8000/docs)
2. Localize e clique no endpoint `PUT /registros/{registro_id}`
3. Clique em "Try it out"
4. No campo `registro_id`, insira o ID do registro que deseja atualizar
5. No editor de JSON, insira os novos dados do registro:

```json
{
  "id_cidade": 1,
  "nome": "Vila Madalena - Atualizado",
  "area": 2.7,
  "imoveis": 3500,
  "populacao": 16000,
  "visitados": true,
  "descricao": "Bairro residencial com muitos bares, restaurantes e galerias de arte"
}
```

6. Clique em "Execute"
7. Observe a resposta. Se a atualização for bem-sucedida, você verá os dados atualizados do registro

## Passo 3: Atualizar o registro usando Python

Vamos criar um script Python simples para atualizar um registro:

```python
import requests
import json
import sys

# Verificar se foi fornecido um ID como argumento
if len(sys.argv) < 2:
    print("Por favor, forneça o ID do registro como argumento.")
    print("Exemplo: python atualizar_registro.py 1")
    sys.exit(1)

# Obter o ID do argumento da linha de comando
registro_id = sys.argv[1]

# URL da API com o ID específico
url = f"http://localhost:8000/registros/{registro_id}"

# Novos dados do registro
registro_atualizado = {
    "id_cidade": 1,
    "nome": "Vila Madalena - Versão Python",
    "area": 2.8,
    "imoveis": 3600,
    "populacao": 17000,
    "visitados": True,
    "descricao": "Bairro atualizado via script Python"
}

# Enviando a requisição PUT
response = requests.put(url, json=registro_atualizado)

# Verificando a resposta
if response.status_code == 200:
    print("Registro atualizado com sucesso!")
    print(json.dumps(response.json(), indent=4))
elif response.status_code == 404:
    print(f"Registro com ID {registro_id} não encontrado.")
else:
    print(f"Erro: {response.status_code}")
    print(response.text)
```

Salve o script acima como `atualizar_registro.py` na pasta `requests_api` e execute:

```bash
python requests_api/atualizar_registro.py 1
```

Substitua `1` pelo ID do registro que você deseja atualizar.

## Passo 4: Verificar as atualizações

Após atualizar um registro, é uma boa prática verificar se as alterações foram aplicadas corretamente:

```bash
# Verificar o registro atualizado
python requests_api/get_registro_by_id.py 1
```

Você deverá ver os novos valores do registro na resposta.

## Tratamento de erros comuns

Ao atualizar registros, você pode encontrar os seguintes erros:

1. **404 Not Found**: O registro com o ID especificado não existe
2. **422 Unprocessable Entity**: Os dados fornecidos não são válidos (tipos incorretos, campos obrigatórios ausentes)
3. **500 Internal Server Error**: Erro no servidor, possivelmente relacionado ao banco de dados

Para cada um desses erros, você deve:

- **404**: Verifique se o ID está correto e se o registro existe
- **422**: Verifique se todos os campos obrigatórios estão presentes e com os tipos corretos
- **500**: Verifique o log do servidor para obter mais detalhes sobre o erro

## Boas práticas para atualizações

1. **Sempre recupere o registro atual antes de atualizá-lo**: Isso evita sobrescrever dados acidentalmente
2. **Atualize apenas os campos necessários**: Embora o PUT exija todos os campos, não altere desnecessariamente os valores
3. **Valide os dados antes de enviar**: Certifique-se de que os dados estão no formato correto
4. **Implemente verificação de concorrência**: Em aplicações de produção, considere usar mecanismos para evitar atualizações simultâneas conflitantes

## Próximos passos

Agora que você sabe como atualizar registros, pode aprender como:

- [Excluindo Registros](07_excluindo_registros.md) - Como remover registros da API