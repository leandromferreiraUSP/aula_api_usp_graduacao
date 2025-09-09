# Criando o Banco de Dados

Neste tutorial, vamos aprender como criar o banco de dados necessário para a API USP Graduação funcionar corretamente. Utilizaremos o script fornecido no projeto e o Alembic para criar as tabelas.

## Passo 1: Executar o script de criação do banco de dados

O projeto inclui um script Python que cria automaticamente o banco de dados `api_db` e o schema `api`. Vamos executá-lo:

```bash
# Certifique-se de que o ambiente virtual está ativado
# No Windows: .venv\Scripts\activate
# No macOS/Linux: source .venv/bin/activate

# Execute o script de criação do banco de dados
python templates/create_db.py
```

Este script faz o seguinte:
1. Conecta-se ao PostgreSQL usando o usuário `postgres` e senha `1234`
2. Verifica se o banco de dados `api_db` já existe
3. Se não existir, cria o banco de dados
4. Conecta-se ao banco de dados `api_db`
5. Cria o schema `api` se não existir

## Passo 2: Configurar o Alembic para migrações

O Alembic é uma ferramenta de migração de banco de dados que usaremos para criar as tabelas. O projeto já vem com o Alembic configurado, mas precisamos copiar o arquivo `env.py` personalizado:

```bash
# Copie o arquivo env.py customizado
cp -f templates/env.py alembic/env.py
```

## Passo 3: Executar as migrações do Alembic

Agora vamos aplicar as migrações para criar as tabelas:

```bash
# Verifique o status atual das migrações
alembic current

# Aplique todas as migrações pendentes
alembic upgrade head
```

Isso criará a tabela `registros` no schema `api` com todos os campos necessários.

## Passo 4: Verificar se a tabela foi criada corretamente

Para confirmar que tudo foi criado corretamente, você pode conectar-se ao banco de dados e verificar:

```bash
# Conecte-se ao banco de dados (substitua 'postgres' pelo seu usuário se necessário)
psql -U postgres -d api_db

# Dentro do psql, execute:
\dn  -- Lista os schemas
\dt api.*  -- Lista as tabelas no schema 'api'
\d api.registros  -- Mostra a estrutura da tabela 'registros'

# Para sair do psql
\q
```

## Entendendo a estrutura da tabela

A tabela `registros` tem a seguinte estrutura:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | Integer | Identificador único do registro (chave primária) |
| id_cidade | Integer | Identificador da cidade |
| nome | String | Nome da cidade |
| area | String | Área específica dentro da cidade |
| imoveis | Integer | Quantidade total de imóveis na área |
| trabalhados | Integer | Quantidade de imóveis já trabalhados |
| nao_trabalhados | Integer | Quantidade de imóveis não trabalhados |
| pend | Float | Percentual de pendência |
| visitados | Integer | Quantidade de imóveis visitados |

## Realizando um reset do banco de dados (se necessário)

Se você precisar recomeçar do zero, pode seguir estes passos:

```bash
# Reverter todas as migrações
alembic downgrade base

# Depois, execute o processo novamente a partir do Passo 1
```

## Próximos passos

Agora que o banco de dados está configurado, você pode prosseguir para:

- [Iniciando a API](03_iniciando_api.md) - Aprenda como iniciar o servidor da API FastAPI.

## Solução de problemas

### Problema: Erro de conexão ao PostgreSQL

Se você ver um erro como `could not connect to server: Connection refused`, verifique:

1. O PostgreSQL está em execução?
2. As credenciais (usuário/senha) estão corretas?
3. O host e a porta estão corretos?

Você pode modificar a conexão no arquivo `templates/create_db.py` se necessário.

### Problema: Erro de permissão ao criar o banco de dados

Se você ver um erro como `permission denied to create database`, o usuário PostgreSQL que você está usando não tem permissões suficientes. Soluções:

1. Use um usuário com permissões de superusuário
2. Conceda permissões ao usuário atual:
   ```sql
   ALTER USER seu_usuario CREATEDB;
   ```

### Problema: Erro nas migrações do Alembic

Se as migrações do Alembic falharem, verifique:

1. O arquivo `alembic.ini` está configurado corretamente?
2. O arquivo `env.py` foi copiado conforme instruído?
3. Os modelos SQLAlchemy em `app/models.py` estão corretos?

Você pode ver mais detalhes sobre o erro usando:

```bash
alembic upgrade head --verbose
```