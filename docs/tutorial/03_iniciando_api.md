# Iniciando a API

Neste tutorial, aprenderemos como iniciar o servidor da API USP Graduação e testar se está funcionando corretamente.

## Pré-requisitos

Antes de iniciar a API, certifique-se de que:
- O ambiente virtual está ativado
- O banco de dados PostgreSQL está em execução
- As migrações do Alembic foram aplicadas (como visto em [Criando o Banco de Dados](02_criando_banco_dados.md))

## Passo 1: Iniciar o servidor da API

O projeto inclui um script Python (`run_api.py`) que inicia o servidor Uvicorn com a aplicação FastAPI. Vamos executá-lo:

```bash
# Certifique-se de que o ambiente virtual está ativado
# No Windows: .venv\Scripts\activate
# No macOS/Linux: source .venv/bin/activate

# Execute o script para iniciar a API
python run_api.py
```

Você deverá ver uma saída semelhante a esta:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Isso significa que a API está em execução e escutando na porta 8000.

## Passo 2: Acessar a documentação interativa

Uma das grandes vantagens do FastAPI é que ele gera automaticamente uma documentação interativa para a API. Você pode acessá-la em:

- [http://localhost:8000/docs](http://localhost:8000/docs) - Documentação Swagger UI
- [http://localhost:8000/redoc](http://localhost:8000/redoc) - Documentação ReDoc

Essas páginas permitem:
- Ver todos os endpoints disponíveis
- Entender os parâmetros e formatos de dados esperados
- Testar os endpoints diretamente no navegador
- Ver os modelos de dados utilizados

## Passo 3: Testar a API manualmente

Vamos fazer um teste simples para verificar se a API está funcionando corretamente:

1. Abra o navegador e acesse [http://localhost:8000/docs](http://localhost:8000/docs)
2. Clique no endpoint `GET /registros/`
3. Clique no botão "Try it out" e depois em "Execute"
4. Você deve receber uma resposta com um array vazio `[]` (pois ainda não há registros no banco de dados)

## Passo 4: Executar a API em modo de desenvolvimento (opcional)

Se você estiver desenvolvendo ou fazendo modificações, pode ser útil executar a API em modo de recarga automática:

```bash
# Usando o Uvicorn diretamente com recarga automática
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Com o modo `--reload`, o servidor reiniciará automaticamente quando detectar alterações nos arquivos Python.

## Entendendo os componentes da API

A API possui os seguintes componentes principais:

- **app/main.py**: Define os endpoints da API
- **app/models.py**: Define os modelos SQLAlchemy
- **app/schemas.py**: Define os schemas Pydantic para validação de dados
- **app/crud.py**: Implementa as operações de banco de dados
- **app/database.py**: Configura a conexão com o banco de dados

## Próximos passos

Agora que a API está em execução, você pode prosseguir para:

- [Criando Registros](04_criando_registros.md) - Aprenda como criar registros na API.

## Solução de problemas

### Problema: Endereço já em uso

Se você ver um erro como `ERROR: [Errno 48] Address already in use`, significa que a porta 8000 já está sendo usada por outro processo. Soluções:

1. Encerre o outro processo que está usando a porta
2. Use uma porta diferente:
   ```bash
   python -c "import uvicorn; uvicorn.run('app.main:app', host='0.0.0.0', port=8001)"
   ```
   ou 
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8001
   ```

### Problema: Erro de conexão com o banco de dados

Se você ver erros relacionados ao banco de dados, verifique:

1. O PostgreSQL está em execução?
2. As credenciais no arquivo `app/database.py` estão corretas?
3. O banco de dados e o schema foram criados corretamente?

### Problema: Warnings do Pydantic

Se você ver avisos como `UserWarning: Valid config keys have changed in V2: * 'orm_mode' has been renamed to 'from_attributes'`, não se preocupe. Estes são apenas avisos de que o projeto está usando uma configuração do Pydantic que foi renomeada na versão 2, mas ainda é compatível.