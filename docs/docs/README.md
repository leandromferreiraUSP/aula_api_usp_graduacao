# Documentação Técnica da API USP Graduação

## Resumo do Projeto

A API USP Graduação é uma API REST desenvolvida com FastAPI que permite gerenciar registros relacionados a imóveis em diferentes áreas de cidades. O sistema utiliza PostgreSQL como banco de dados, SQLAlchemy como ORM (Object-Relational Mapping) e Alembic para migrações de banco de dados. A API oferece endpoints para criar, ler, buscar e deletar registros, com validação de dados através do Pydantic.

## Abstrações Principais

1. [**Registro**](01_registro.md) - Entidade principal que representa os dados de imóveis/áreas
2. [**Database**](02_database.md) - Camada de acesso ao banco de dados PostgreSQL
3. [**API Endpoints**](03_api_endpoints.md) - Interface REST para manipulação dos registros
4. [**Operações CRUD**](04_operacoes_crud.md) - Operações de banco de dados para gerenciar registros
5. [**Validação de Esquema**](05_validacao_esquema.md) - Validação de dados com Pydantic
6. [**Sistema de Migração**](06_sistema_migracao.md) - Sistema de migração de banco de dados com Alembic
7. [**Requisições de Cliente**](07_requisicoes_cliente.md) - Scripts para interação com a API

## Diagramas de Arquitetura

### Diagrama de Relacionamento de Abstrações

```mermaid
flowchart TB
    API[API Endpoints] --> CRUD[Operações CRUD]
    API --> Schema[Validação de Esquema]
    CRUD --> DB[Database]
    DB --> Registro[Registro]
    Schema --> Registro
    Migration[Sistema de Migração] --> DB
    Client[Requisições de Cliente] --> API
```

### Diagrama de Fluxo da Aplicação

```mermaid
flowchart LR
    A[Cliente] -->|Requisição| B[API Endpoint]
    B -->|Validação| C[Schema Pydantic]
    C -->|Dados Validados| D[Operações CRUD]
    D -->|Query SQL| E[Database]
    E -->|Resultado| D
    D -->|Dados| B
    B -->|Resposta| A
    F[Script de Criação DB] -->|Criar| E
    G[Migrações Alembic] -->|Aplicar| E
```

### Diagrama de Sequência

```mermaid
sequenceDiagram
    participant U as Usuário
    participant C as Cliente (Script)
    participant A as API Endpoints
    participant S as Schema Validation
    participant CR as CRUD Operations
    participant DB as Database
    
    U->>C: Executa Script
    C->>A: Envia Requisição
    A->>S: Valida Dados
    S-->>A: Dados Validados
    A->>CR: Chama Operação
    CR->>DB: Executa Query
    DB-->>CR: Retorna Resultado
    CR-->>A: Retorna Dados
    A-->>C: Retorna Resposta
    C-->>U: Exibe Resultado
```

## Índice da Documentação

- [Registro](01_registro.md)
- [Database](02_database.md)
- [API Endpoints](03_api_endpoints.md)
- [Operações CRUD](04_operacoes_crud.md)
- [Validação de Esquema](05_validacao_esquema.md)
- [Sistema de Migração](06_sistema_migracao.md)
- [Requisições de Cliente](07_requisicoes_cliente.md)