# Erros Comuns e Soluções

Neste tutorial, abordaremos os erros mais comuns que você pode encontrar ao utilizar a API USP Graduação e suas respectivas soluções.

## Pré-requisitos

Antes de começar, recomenda-se que você tenha:

- Concluído os tutoriais anteriores para entender o funcionamento básico da API
- Familiaridade com os códigos de status HTTP e seu significado

## Entendendo os códigos de status HTTP

A API USP Graduação utiliza códigos de status HTTP padrão para indicar o resultado das requisições:

| Código | Significado | Interpretação |
|--------|-------------|---------------|
| 200 | OK | A requisição foi bem-sucedida |
| 201 | Created | Um novo recurso foi criado com sucesso |
| 400 | Bad Request | A requisição foi malformada |
| 404 | Not Found | O recurso solicitado não existe |
| 422 | Unprocessable Entity | Os dados enviados são inválidos |
| 500 | Internal Server Error | Ocorreu um erro no servidor |

## Erro 1: Banco de dados indisponível

**Sintoma**: Ao tentar acessar qualquer endpoint da API, você recebe um erro 500 (Internal Server Error).

**Possíveis causas**:
1. O container Docker do PostgreSQL não está em execução
2. As configurações de conexão no arquivo `app/database.py` estão incorretas
3. O banco de dados existe, mas o schema ou a tabela não foram criados

**Soluções**:

1. **Verificar status do container Docker**:
   ```bash
   docker ps
   ```
   Se o container não estiver listado, inicie-o:
   ```bash
   docker start <nome_do_container>
   ```
   Se estiver usando Colima:
   ```bash
   colima start
   ```

2. **Verificar as configurações de conexão**:
   Abra o arquivo `app/database.py` e verifique se a string de conexão está correta:
   ```python
   SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"
   ```

3. **Aplicar as migrações do Alembic**:
   ```bash
   alembic upgrade head
   ```

4. **Verificar logs da API para mensagens de erro mais detalhadas**:
   Analise a saída do terminal onde a API está sendo executada para identificar mensagens de erro específicas.

## Erro 2: Registro não encontrado (404)

**Sintoma**: Ao tentar acessar, atualizar ou excluir um registro específico, você recebe um erro 404 (Not Found).

**Possíveis causas**:
1. O ID fornecido não existe no banco de dados
2. O registro foi excluído previamente
3. Você está usando um endpoint incorreto

**Soluções**:

1. **Verificar se o registro existe**:
   ```bash
   # Listar todos os registros para confirmar os IDs disponíveis
   python requests_api/get_registros.py
   ```

2. **Verificar o formato do endpoint**:
   Certifique-se de que está usando o formato correto:
   - Correto: `http://localhost:8000/registros/1`
   - Incorreto: `http://localhost:8000/registros/1/`

3. **Criar um novo registro se necessário**:
   Se o registro foi excluído, você precisará criar um novo.

## Erro 3: Validação de dados (422)

**Sintoma**: Ao tentar criar ou atualizar um registro, você recebe um erro 422 (Unprocessable Entity).

**Possíveis causas**:
1. Campos obrigatórios estão ausentes
2. Tipos de dados incorretos (por exemplo, texto em um campo numérico)
3. Valores fora dos limites aceitáveis

**Soluções**:

1. **Verificar o modelo de dados**:
   Revise os requisitos para cada campo no schema:
   ```python
   # De app/schemas.py
   class RegistroBase(BaseModel):
       id_cidade: int
       nome: str
       area: float
       imoveis: int
       populacao: int
       visitados: bool
       descricao: Optional[str] = None
   ```

2. **Verificar a mensagem de erro detalhada**:
   O erro 422 geralmente vem acompanhado de uma mensagem que indica exatamente qual campo está com problema.

3. **Exemplo de dados válidos**:
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

## Erro 4: Problemas de conexão

**Sintoma**: A API não responde ou você recebe erros de conexão como "Connection refused".

**Possíveis causas**:
1. A API não está em execução
2. A API está rodando em uma porta ou host diferente
3. Problemas de rede ou firewall

**Soluções**:

1. **Verificar se a API está em execução**:
   Verifique o terminal onde você iniciou a API ou execute:
   ```bash
   # Verificar processos Python em execução
   ps aux | grep python
   ```

2. **Verificar a porta configurada**:
   A API deve estar rodando na porta 8000 por padrão. Verifique o arquivo `run_api.py`:
   ```python
   uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
   ```

3. **Tentar acessar pelo navegador**:
   Tente acessar `http://localhost:8000/docs` diretamente no navegador para verificar se a API está respondendo.

## Erro 5: Incompatibilidade de versões

**Sintoma**: Avisos ou erros relacionados a bibliotecas, especialmente relacionados ao Pydantic ou SQLAlchemy.

**Possíveis causas**:
1. Versões diferentes das bibliotecas usadas no desenvolvimento
2. Mudanças nas APIs das bibliotecas entre versões

**Soluções**:

1. **Verificar as dependências instaladas**:
   ```bash
   pip list
   ```

2. **Instalar versões específicas se necessário**:
   ```bash
   pip install pydantic==2.0.3
   pip install sqlalchemy==2.0.23
   ```

3. **Para avisos de Pydantic V2**:
   Se você ver avisos sobre `orm_mode` sendo renomeado para `from_attributes`, você pode atualizar o código:
   
   De:
   ```python
   class Config:
       orm_mode = True
   ```
   
   Para:
   ```python
   class Config:
       from_attributes = True
   ```

## Dicas para depuração eficaz

1. **Use logs**: Adicione logs temporários para rastrear o fluxo de execução e valores de variáveis
2. **Verifique a resposta completa**: As respostas de erro geralmente contêm informações detalhadas sobre o problema
3. **Use ferramentas como Postman ou Insomnia**: Elas oferecem mais detalhes sobre as requisições e respostas
4. **Verifique o esquema do banco de dados**: Use um cliente SQL para verificar diretamente o estado do banco de dados

## Próximos passos

Com o conhecimento para identificar e resolver problemas comuns, você está pronto para explorar:

- [Guia de Testes](09_guia_testes.md) - Como testar a API de forma eficiente