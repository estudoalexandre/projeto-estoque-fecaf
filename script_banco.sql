-- Criação do banco de dados
CREATE DATABASE projeto_estoque;

-- Seleciona o banco para uso
USE projeto_estoque;

-- Criação da tabela Usuario
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    confirm_password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    nivel_funcao VARCHAR(15) NOT NULL DEFAULT 'comum'
);

-- Criação da tabela Produto
CREATE TABLE produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    quantidade INT NOT NULL,
    minimo_estoque INT NOT NULL,
    preco_unitario FLOAT NOT NULL,
    data_entrada DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Criação da tabela SaidaProduto
CREATE TABLE saida_produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL,
    data_saida DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    motivo VARCHAR(150) DEFAULT 'venda',
    FOREIGN KEY (produto_id) REFERENCES produto(id) ON DELETE CASCADE
);
