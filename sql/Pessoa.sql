CREATE TABLE Pessoa(
    cpf_cnpj VARCHAR(14) PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    senha VARCHAR(100),
    nivel INT
);
INSERT INTO Pessoa(
    cpf_cnpj,
    nome,
    email,
    senha,
    nivel
) VALUES(
    '11111111111',
    'Admin',
    'admin@desafio-t10.com',
    '!5q%IYk0Hy',
    5
)