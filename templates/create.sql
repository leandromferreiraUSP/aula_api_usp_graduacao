CREATE SCHEMA IF NOT EXISTS api;

CREATE TABLE api.registros (
    id SERIAL PRIMARY KEY,
    id_cidade INTEGER,
    nome VARCHAR,
    area VARCHAR,
    imoveis INTEGER,
    trabalhados INTEGER,
    nao_trabalhados INTEGER,
    pend FLOAT,
    visitados INTEGER
);