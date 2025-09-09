# Excluindo Registros

Neste tutorial, aprenderemos como excluir registros na API USP Graduação.

## Pré-requisitos

Antes de começar, certifique-se de que:

- A API está em execução (como explicado em [Iniciando a API](03_iniciando_api.md))
- Existem registros no banco de dados (como explicado em [Criando Registros](04_criando_registros.md))
- Você sabe como consultar registros (como explicado em [Consultando Registros](05_consultando_registros.md))

## Entendendo a exclusão de registros

Na API USP Graduação, a exclusão de registros é realizada através do método DELETE. Este processo:

- É irreversível - uma vez excluído, o registro não pode ser recuperado
- Requer apenas o ID do registro a ser excluído
- Retorna o registro excluído como confirmação

## Passo 1: Identificar o registro a ser excluído

Primeiro, você precisa identificar qual registro deseja excluir. Liste os registros disponíveis para encontrar o ID correto:

```bash
# Listar todos os registros
python requests_api/get_registros.py
```

Anote o ID do registro que você deseja excluir.

## Passo 2: Excluir o registro usando a interface Swagger

1. Abra o navegador e acesse [http://localhost:8000/docs](http://localhost:8000/docs)
2. Localize e clique no endpoint `DELETE /registros/{registro_id}`
3. Clique em "Try it out"
4. No campo `registro_id`, insira o ID do registro que deseja excluir
5. Clique em "Execute"
6. Observe a resposta. Se a exclusão for bem-sucedida, você verá os dados do registro que foi removido

## Passo 3: Excluir o registro usando Python

A API inclui um script de exemplo para excluir registros. Vamos analisar o arquivo `requests_api/delete_registro.py`:

```python
import requests
import json
import sys

# Verificar se foi fornecido um ID como argumento
if len(sys.argv) < 2:
    print("Por favor, forneça o ID do registro como argumento.")
    print("Exemplo: python delete_registro.py 1")
    sys.exit(1)

# Obter o ID do argumento da linha de comando
registro_id = sys.argv[1]

# URL da API com o ID específico
url = f"http://localhost:8000/registros/{registro_id}"

# Enviando a requisição DELETE
response = requests.delete(url)

# Verificando a resposta
if response.status_code == 200:
    print("Registro excluído com sucesso!")
    print(json.dumps(response.json(), indent=4))
elif response.status_code == 404:
    print(f"Registro com ID {registro_id} não encontrado.")
else:
    print(f"Erro: {response.status_code}")
    print(response.text)
```

Para executar este script:

```bash
python requests_api/delete_registro.py 1
```

Substitua `1` pelo ID do registro que você deseja excluir.

## Passo 4: Verificar a exclusão

Após excluir um registro, é importante verificar se ele realmente foi removido do banco de dados:

```bash
# Tentar buscar o registro excluído
python requests_api/get_registro_by_id.py 1
```

Se a exclusão foi bem-sucedida, você receberá uma mensagem de erro 404 indicando que o registro não foi encontrado.

## Exclusões em massa (considerações)

A API atual não possui um endpoint para exclusões em massa. Se você precisar excluir vários registros, terá que fazer isso um por um.

Para cenários de produção onde a exclusão em massa é necessária, considere:

1. Implementar um endpoint específico para exclusão em lote
2. Usar transações de banco de dados para garantir que todas as exclusões sejam concluídas ou nenhuma seja aplicada
3. Adicionar um mecanismo de exclusão lógica (marcar como excluído em vez de remover fisicamente)

## Tratamento de erros

Os principais erros que você pode encontrar ao excluir registros são:

1. **404 Not Found**: O registro com o ID especificado não existe ou já foi excluído
2. **500 Internal Server Error**: Erro no servidor, possivelmente relacionado ao banco de dados

Como lidar com esses erros:

- **404**: Verifique se o ID está correto e se o registro existe
- **500**: Verifique o log do servidor para mais detalhes sobre o erro

## Boas práticas para exclusões

1. **Confirmação**: Em aplicações reais, sempre solicite confirmação do usuário antes de excluir registros
2. **Backup**: Considere fazer backup dos dados antes de excluí-los em ambientes de produção
3. **Logs**: Mantenha logs de todas as operações de exclusão para fins de auditoria
4. **Exclusão lógica**: Em muitos casos, é preferível implementar uma exclusão lógica (marcar como inativo) em vez de uma exclusão física

## Próximos passos

Agora que você aprendeu as operações básicas CRUD (Create, Read, Update, Delete), pode avançar para:

- [Erros Comuns e Soluções](08_erros_e_solucoes.md) - Como lidar com problemas frequentes na API