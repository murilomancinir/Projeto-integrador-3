-- =========================================================
-- BANCO DE DADOS - PROJETO Logística
-- PostgreSQL
-- Estrutura inicial
-- =========================================================

-- =========================================
-- 1. CRIAÇÃO DO USUÁRIO
-- =========================================

CREATE ROLE fretes WITH LOGIN PASSWORD '1234';

-- =========================================
-- 2. CRIAÇÃO DO BANCO
-- =========================================

CREATE DATABASE frete
    WITH
    OWNER = fretes
    ENCODING = 'UTF8'
    LC_COLLATE = 'Portuguese_Brazil.1252'
    LC_CTYPE = 'Portuguese_Brazil.1252'
    TEMPLATE = template0;
-- Conectar no bano frete para seguir par o proximo passo

-- =========================================
-- 3. TABELA DE CLIENTES
-- =========================================
CREATE TABLE clientes (
    id_cliente INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(150),
    documento VARCHAR(20),
    endereco VARCHAR(150),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    observacao VARCHAR(500),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
select * from clientes
-- =========================================
-- 4. TABELA DE MOTORISTAS
-- =========================================
CREATE TABLE motoristas (
    id_motorista INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    telefone VARCHAR(20),
    cnh VARCHAR(30),
    validade_cnh DATE,
    observacao VARCHAR(500),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
select * from motoristas

delete from motoristas where id_motorista = 2
-- =========================================
-- 5. TABELA DE VEÍCULOS
-- =========================================
CREATE TABLE veiculos (
    id_veiculo INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    placa VARCHAR(10) NOT NULL UNIQUE,
    modelo VARCHAR(100) NOT NULL,
    marca VARCHAR(100),
    ano INTEGER,
    consumo_medio NUMERIC(10,2),
    observacao VARCHAR(500),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- 6. TABELA DE SERVIÇOS / VIAGENS
-- =========================================
CREATE TABLE servicos (
    id_servico INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    id_motorista INTEGER NOT NULL,
    id_veiculo INTEGER NOT NULL,

    origem VARCHAR(150) NOT NULL,
    destino VARCHAR(150) NOT NULL,
    distancia_km NUMERIC(10,2),
    consumo_km_l NUMERIC(10,2),
    valor_combustivel NUMERIC(10,2),
    outras_despesas NUMERIC(10,2) ,
    custo_combustivel NUMERIC(10,2),
    custo_total NUMERIC(10,2),

    observacao VARCHAR(500),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_servicos_clientes
        FOREIGN KEY (id_cliente)
        REFERENCES clientes (id_cliente),

    CONSTRAINT fk_servicos_motoristas
        FOREIGN KEY (id_motorista)
        REFERENCES motoristas (id_motorista),

    CONSTRAINT fk_servicos_veiculos
        FOREIGN KEY (id_veiculo)
        REFERENCES veiculos (id_veiculo)
);

-- =========================================
-- 7. ÍNDICES 
-- =========================================
CREATE INDEX idx_clientes_nome ON clientes (nome);
CREATE INDEX idx_motoristas_nome ON motoristas (nome);
CREATE INDEX idx_veiculos_placa ON veiculos (placa);
CREATE INDEX idx_servicos_data_cadastro ON servicos (data_cadastro);
CREATE INDEX idx_servicos_cliente ON servicos (id_cliente);
CREATE INDEX idx_servicos_motorista ON servicos (id_motorista);
CREATE INDEX idx_servicos_veiculo ON servicos (id_veiculo);

-- =========================================
-- 8. EXEMPLOS DE CONSULTAS
-- =========================================

-- Listar clientes ativos
-- SELECT * FROM clientes WHERE ativo = TRUE ORDER BY nome;

-- Listar motoristas ativos
-- SELECT * FROM motoristas WHERE ativo = TRUE ORDER BY nome;

-- Listar veículos ativos
-- SELECT * FROM veiculos WHERE ativo = TRUE ORDER BY modelo;

-- Listar serviços com nome do cliente, motorista e veículo
-- SELECT
--     s.id_servico,
--     c.nome AS cliente,
--     m.nome AS motorista,
--     v.placa AS veiculo,
--     s.origem,
--     s.destino,
--     s.distancia_km,
--     s.custo_total,
--     s.data_cadastro
-- FROM servicos s
-- INNER JOIN clientes c ON c.id_cliente = s.id_cliente
-- INNER JOIN motoristas m ON m.id_motorista = s.id_motorista
-- INNER JOIN veiculos v ON v.id_veiculo = s.id_veiculo
-- WHERE s.ativo = TRUE
-- ORDER BY s.id_servico DESC;