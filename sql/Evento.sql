CREATE TABLE Evento(
    id CHAR(36) PRIMARY KEY,
    dt_evento DATE ,
    usuario VARCHAR(14),
    solicitacao CHAR(36),
    situacao INT ,
    FOREIGN KEY (solicitacao) REFERENCES Solicitacao,
    FOREIGN KEY (usuario) REFERENCES Pessoa
)