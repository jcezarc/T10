# Desafio T10

#####  por: `Júlio Cascalles`

```
Este projeto demonstra funções básicas de uma API para acompanhamento de solicitações de produtos.
```

---

### Banco de dados
* Esta API foi feita para rodar com Postgres (e os testes unitários com Sqlite)
    - Se quiser mudar de Postgres para MongoDb, abra o arquivo `/backend/service/db_connection.py` e troque o DAO SqlTable para MongoTable.
* Variáveis de ambiente (para usar com Postgres)
    - T10_USER
    - T10_HOST
    - T10_PASSWORD
    - T10_DATA_BASE
* Tabelas
![](./doc/banco_de_dados.png)

---
* ### Como rodar:
    * Execute os scripts da pasta SQL no banco "T10" do seu servidor
    * Configure as variáveis de ambiente no seu sistema operacional -- Exemplo:
        - `SET T10_USER=root`
        - `SET T10_HOST=localhost`
        - `SET T10_PASSWORD=xyz1234`
        - `SET T10_DATA_BASE=julio`
    * Instale as dependências necessárias do Python, com...
        - `pip install -r requirements.txt`
    * Rode o back-end com...
        - `python app.py`

> Se você estiver usando Windows, disponibilizei o arquivo de lote `RUN.bat` para rodar a API.

---

### Rotas
* `/docs` Traz a documentação _Swagger_ com todos os verbos REST disponíveis para a API e exemplos funcionais 
![](./doc/Swagger.png)

* `/T10/Pessoa` Pode ser usado para trazer várias pessoas (onde você pode passar uma query com os nomes dos campos, p.ex.: `...?nome=PESSOAxyz`)
    * você pode também passar o `.../<cpf_cnpj>` para operações que exigem um registro único
    (consula por campo chave ou exclusão)

* `/T10/Evento` Permite gravar ou consultar um evento, de acordo com as permissões do usuário.

---

### Testes unitários
As seguintes situações foram testadas para verificar se cada serviço está funcionando conforme esperado:


* Falha na busca: Deve retornar o status 404 quando não encontra o registro
* Sucesso na busca: Retorna o registro relacionado ao campo chave usado na busca;
* Falha de inclusão: Não permite registro com campos inválidos;
* Sucesso na inclusão: Simula a gravação de um registro e retorna sem erros;
* Falha na alteração: Não permite registro com campos inválidos;
* Sucesso na alteração: Altera o registro, localiza ele no banco de dados e compara com o esperado.


![](./doc/testes_unitarios.png)

---

### Testes funcionais
Com a API rodando, o roteiro abaixo é executado, usando-se o comando `python simulador.py` :

![](./doc/testes_funcionais.png)

#### **Roteiro de testes:**

1)
2)
3)
...