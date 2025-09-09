# Guia de Testes

Neste tutorial, aprenderemos como testar a API USP Graduação, tanto manualmente quanto com scripts automatizados.

## Pré-requisitos

Antes de começar, certifique-se de que:

- A API está em execução (como explicado em [Iniciando a API](03_iniciando_api.md))
- O banco de dados PostgreSQL está funcionando
- Você compreende os conceitos básicos de testes de API

## Importância dos testes

Testar sua API é crucial para:

- Garantir que todas as funcionalidades estejam operando corretamente
- Identificar problemas rapidamente após alterações no código
- Documentar o comportamento esperado da API
- Facilitar a manutenção e evolução do sistema

## Tipos de testes

Para a API USP Graduação, podemos realizar os seguintes tipos de testes:

1. **Testes manuais**: Usando a interface Swagger ou ferramentas como Postman
2. **Testes automatizados com scripts**: Usando os scripts Python fornecidos na pasta `requests_api`
3. **Testes unitários**: Para componentes individuais (não implementados neste projeto)
4. **Testes de integração**: Para verificar a integração entre a API e o banco de dados

## Passo 1: Testes manuais usando Swagger

O FastAPI fornece uma interface Swagger que permite testar todos os endpoints facilmente:

1. Acesse `http://localhost:8000/docs`
2. Explore cada endpoint disponível
3. Use a função "Try it out" para enviar requisições
4. Verifique as respostas e códigos de status

Este método é excelente para testes exploratórios e para entender o comportamento da API.

## Passo 2: Testes com scripts Python

O diretório `requests_api` contém scripts Python para testar cada endpoint da API. Vamos usar estes scripts para realizar um teste completo:

### Preparação (limpeza)

Primeiro, vamos excluir quaisquer registros existentes para começar com um banco de dados limpo:

```bash
# Listar os registros existentes para obter os IDs
python requests_api/get_registros.py

# Excluir cada registro (repita para cada ID)
python requests_api/delete_registro.py 1
python requests_api/delete_registro.py 2
# ... e assim por diante para todos os registros
```

### Teste de criação

Agora, vamos criar novos registros:

```bash
# Criar um registro individual
python requests_api/create_registro.py

# Criar múltiplos registros
python requests_api/create_registro_batch.py
```

Verifique se os registros foram criados corretamente:

```bash
python requests_api/get_registros.py
```

### Teste de consulta

Teste as diferentes formas de consultar registros:

```bash
# Obter todos os registros
python requests_api/get_registros.py

# Obter um registro específico por ID
# Substitua 1 pelo ID de um registro existente
python requests_api/get_registro_by_id.py 1

# Obter registros por cidade
# Substitua 1 pelo ID de uma cidade existente
python requests_api/get_registro_cidade.py 1

# Buscar por status de visitados
python requests_api/search_by_visitados.py true
python requests_api/search_by_visitados.py false
```

### Teste de atualização

Para testar a atualização, você precisará criar um script semelhante ao apresentado no tutorial [Atualizando Registros](06_atualizando_registros.md):

```bash
# Criar um script de atualização e executá-lo
# Substitua 1 pelo ID de um registro existente
python requests_api/atualizar_registro.py 1
```

### Teste de exclusão

Por fim, teste a exclusão de registros:

```bash
# Excluir um registro específico
# Substitua 1 pelo ID de um registro existente
python requests_api/delete_registro.py 1

# Verificar se o registro foi excluído
python requests_api/get_registro_by_id.py 1  # Deve retornar 404
```

## Passo 3: Criando um script de teste completo

Você pode criar um script que teste automaticamente todos os aspectos da API. Abaixo está um exemplo básico:

```python
import requests
import json
import time

# Configurações
BASE_URL = "http://localhost:8000"
VERBOSE = True  # Define se informações detalhadas serão exibidas

def log(message):
    """Exibe mensagem se VERBOSE for True"""
    if VERBOSE:
        print(message)

def test_api():
    """Executa testes completos na API"""
    
    # Contador de testes
    tests_passed = 0
    tests_failed = 0
    
    log("Iniciando testes da API USP Graduação...")
    
    # Teste 1: Verificar se a API está online
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            log("✅ API está online")
            tests_passed += 1
        else:
            log(f"❌ API não está respondendo corretamente: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        log(f"❌ Erro ao conectar à API: {str(e)}")
        tests_failed += 1
        return tests_passed, tests_failed
    
    # Teste 2: Criar um registro
    try:
        novo_registro = {
            "id_cidade": 999,
            "nome": "Local de Teste",
            "area": 1.5,
            "imoveis": 100,
            "populacao": 500,
            "visitados": True,
            "descricao": "Local criado para testes automatizados"
        }
        
        response = requests.post(f"{BASE_URL}/registros/", json=novo_registro)
        
        if response.status_code == 200:
            registro_criado = response.json()
            log(f"✅ Registro criado com ID: {registro_criado['id']}")
            tests_passed += 1
            
            # Armazenar ID para testes subsequentes
            registro_id = registro_criado['id']
        else:
            log(f"❌ Falha ao criar registro: {response.status_code}")
            log(response.text)
            tests_failed += 1
            return tests_passed, tests_failed
    except Exception as e:
        log(f"❌ Erro ao criar registro: {str(e)}")
        tests_failed += 1
        return tests_passed, tests_failed
    
    # Teste 3: Buscar o registro criado
    try:
        response = requests.get(f"{BASE_URL}/registros/{registro_id}")
        
        if response.status_code == 200:
            registro = response.json()
            if registro['nome'] == novo_registro['nome']:
                log("✅ Busca por ID funcionando corretamente")
                tests_passed += 1
            else:
                log("❌ Dados do registro não correspondem ao enviado")
                tests_failed += 1
        else:
            log(f"❌ Falha ao buscar registro: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        log(f"❌ Erro ao buscar registro: {str(e)}")
        tests_failed += 1
    
    # Teste 4: Atualizar o registro
    try:
        registro_atualizado = novo_registro.copy()
        registro_atualizado['nome'] = "Local de Teste - Atualizado"
        registro_atualizado['visitados'] = False
        
        response = requests.put(f"{BASE_URL}/registros/{registro_id}", json=registro_atualizado)
        
        if response.status_code == 200:
            registro = response.json()
            if registro['nome'] == registro_atualizado['nome'] and registro['visitados'] == False:
                log("✅ Atualização funcionando corretamente")
                tests_passed += 1
            else:
                log("❌ Atualização não aplicou todas as mudanças")
                tests_failed += 1
        else:
            log(f"❌ Falha ao atualizar registro: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        log(f"❌ Erro ao atualizar registro: {str(e)}")
        tests_failed += 1
    
    # Teste 5: Buscar por filtro de cidade
    try:
        response = requests.get(f"{BASE_URL}/registros/cidade/999")
        
        if response.status_code == 200:
            registros = response.json()
            if len(registros) > 0 and registros[0]['id_cidade'] == 999:
                log("✅ Busca por cidade funcionando corretamente")
                tests_passed += 1
            else:
                log("❌ Busca por cidade não retornou os dados esperados")
                tests_failed += 1
        else:
            log(f"❌ Falha na busca por cidade: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        log(f"❌ Erro na busca por cidade: {str(e)}")
        tests_failed += 1
    
    # Teste 6: Busca por status de visitados
    try:
        response = requests.get(f"{BASE_URL}/registros/search/?visitados=false")
        
        if response.status_code == 200:
            registros = response.json()
            if len(registros) > 0 and not registros[0]['visitados']:
                log("✅ Busca por status de visitados funcionando corretamente")
                tests_passed += 1
            else:
                log("❌ Busca por status de visitados não retornou os dados esperados")
                tests_failed += 1
        else:
            log(f"❌ Falha na busca por status de visitados: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        log(f"❌ Erro na busca por status de visitados: {str(e)}")
        tests_failed += 1
    
    # Teste 7: Excluir o registro criado
    try:
        response = requests.delete(f"{BASE_URL}/registros/{registro_id}")
        
        if response.status_code == 200:
            log("✅ Exclusão funcionando corretamente")
            tests_passed += 1
            
            # Verificar se o registro foi realmente excluído
            response = requests.get(f"{BASE_URL}/registros/{registro_id}")
            if response.status_code == 404:
                log("✅ Registro realmente excluído")
                tests_passed += 1
            else:
                log("❌ Registro ainda existe após exclusão")
                tests_failed += 1
        else:
            log(f"❌ Falha ao excluir registro: {response.status_code}")
            tests_failed += 1
    except Exception as e:
        log(f"❌ Erro ao excluir registro: {str(e)}")
        tests_failed += 1
    
    # Resultados finais
    log("\n----- RESULTADOS DOS TESTES -----")
    log(f"Testes bem-sucedidos: {tests_passed}")
    log(f"Testes falhos: {tests_failed}")
    log(f"Total de testes: {tests_passed + tests_failed}")
    
    return tests_passed, tests_failed

if __name__ == "__main__":
    test_api()
```

Salve este script como `test_api_completo.py` e execute-o para realizar um teste completo da API:

```bash
python test_api_completo.py
```

## Boas práticas para testes

1. **Teste em ambiente isolado**: Use um banco de dados separado para testes
2. **Automatize os testes**: Crie scripts que possam ser executados regularmente
3. **Teste casos de erro**: Verifique como a API se comporta quando recebe dados inválidos
4. **Teste limites**: Teste com valores limítrofes (máximos, mínimos, etc.)
5. **Mantenha registros**: Salve logs dos testes para análise posterior
6. **Teste de carga**: Para APIs em produção, teste o comportamento sob carga elevada

## Ferramentas adicionais para testes

Além dos scripts básicos, você pode usar ferramentas mais avançadas:

- **Pytest**: Framework de teste Python para testes mais estruturados
- **Locust**: Ferramenta para testes de carga
- **Postman**: Interface gráfica para testes de API com capacidade de automação
- **Newman**: CLI para rodar coleções do Postman em ambientes de integração contínua

## Conclusão

Os testes são uma parte fundamental do desenvolvimento de APIs. Com os conhecimentos adquiridos neste tutorial, você pode garantir que a API USP Graduação funcione corretamente e identificar problemas rapidamente.

Parabéns por concluir toda a série de tutoriais! Agora você tem um entendimento completo sobre como usar e manter a API USP Graduação.