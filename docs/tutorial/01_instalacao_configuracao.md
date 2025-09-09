# Instalação e Configuração

Neste guia, vamos configurar o ambiente necessário para executar a API USP Graduação.

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

1. Python 3.12 ou superior
2. PostgreSQL 12 ou superior
3. Git (opcional, mas recomendado)

## Passo 1: Clonar ou baixar o repositório

Se você tem Git instalado:

```bash
git clone https://github.com/seu-usuario/aula_api_usp_graduacao.git
cd aula_api_usp_graduacao
```

Ou você pode baixar o arquivo ZIP do repositório e extraí-lo.

## Passo 2: Criar um ambiente virtual Python

É uma boa prática usar ambientes virtuais para projetos Python. Vamos criar um:

```bash
# Criar o ambiente virtual
python -m venv .venv

# Ativar o ambiente virtual
# No Windows:
.venv\Scripts\activate
# No macOS/Linux:
source .venv/bin/activate
```

## Passo 3: Instalar as dependências

O projeto utiliza várias bibliotecas Python que precisam ser instaladas:

```bash
# Instalar as dependências
pip install -r requirements.txt
```

Ou você pode instalar as dependências individualmente:

```bash
pip install fastapi>=0.115.0,<0.116.0
pip install uvicorn>=0.30.6,<0.31.0
pip install sqlalchemy>=2.0.35,<2.1.0
pip install alembic>=1.13.3,<1.14.0
pip install psycopg2-binary>=2.9.9,<2.10.0
pip install requests>=2.32.3,<2.33.0
```

## Passo 4: Configurar o banco de dados PostgreSQL

Certifique-se de que o PostgreSQL esteja em execução e acessível.

Você pode usar o Docker para iniciar o PostgreSQL (opcional, se preferir não instalar localmente):

```bash
docker run --name postgresql -e POSTGRES_PASSWORD=1234 -p 5432:5432 -d postgres
```

## Passo 5: Verificar a configuração

Vamos verificar se tudo está configurado corretamente:

1. Verifique se o ambiente virtual está ativo:
   - Deve aparecer `(.venv)` no início da linha de comando

2. Verifique se o PostgreSQL está acessível:
   ```bash
   # No Windows (você pode precisar instalar o cliente psql separadamente)
   psql -U postgres -h localhost -c "SELECT version();"

   # No macOS/Linux
   psql -U postgres -h localhost -c "SELECT version();"
   ```

   Quando solicitado, use a senha `1234` (ou a senha que você configurou).

3. Verifique se as dependências foram instaladas:
   ```bash
   pip list
   ```
   
   Você deve ver packages como `fastapi`, `uvicorn`, `sqlalchemy`, `alembic`, etc.

## Próximos passos

Agora que você tem o ambiente configurado, pode prosseguir para:

- [Criando o Banco de Dados](02_criando_banco_dados.md) - Aprenda a criar o banco de dados e as tabelas necessárias.

## Solução de problemas

### Problema: Erro ao instalar psycopg2-binary

Se você encontrar erros ao instalar `psycopg2-binary`, pode ser necessário instalar algumas dependências do sistema:

**No Ubuntu/Debian:**
```bash
sudo apt-get install libpq-dev python3-dev
```

**No macOS (com Homebrew):**
```bash
brew install postgresql
```

**No Windows:**
Geralmente, a versão binária (`psycopg2-binary`) funciona sem problemas.

### Problema: PostgreSQL não está acessível

Verifique se o PostgreSQL está em execução:

**No Ubuntu/Debian:**
```bash
sudo systemctl status postgresql
```

**No macOS (com Homebrew):**
```bash
brew services list | grep postgres
```

**No Windows:**
Verifique o "Gerenciador de Serviços" e certifique-se de que o serviço PostgreSQL está em execução.