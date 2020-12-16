'''
Executa os testes funcionais da API,
cumprindo um roteiro de chamadas e
avaliando o retorno de cada uma delas.
'''

import requests
from faker import Faker


BASE_URL = 'http://localhost/T10/{}'


class Simulador:

    def __init__(self, faker):
        self.faker = faker
        self.token = None

    def login(self, usuario, senha):
        record = {}
        print('\n*** Testes funcionais para o desafio T10 ***')
        print('Aguarde...')
        record['usuario'] = usuario
        record['senha'] = senha
        url = BASE_URL.format('login')
        resp = requests.post(url, json=record)
        assert resp.status_code == 200
        self.token = resp.text

    def autenticacao(self):
        return {'Authorization': self.token}

    def cria_pessoa(self, id, nivel):
        record = {}
        fake = self.faker
        print('-'*50)
        print('[POST]', id)
        record['cpf_cnpj'] = id
        record['nome'] = fake.name()
        record['email'] = fake.email()
        record['nivel'] = nivel
        resp = requests.post(
            BASE_URL.format('Pessoa'),
            json=record,
            header=self.autenticacao()
        )
        assert resp.status_code == 201

    def fazer_solicitacao(self, id):
        record = {}
        fake = self.faker
        print('-'*50)
        print('[POST]', id)
        record['id'] = id
        record['conta'] = fake.credit_card_number()
        record['detalhes'] = fake.text(200)
        resp = requests.post(
            BASE_URL.format('Solicitacao'),
            json=record,
            header=self.autenticacao()
        )
        assert resp.status_code == 201

    def run(self):
        self.login('admin@desafio-t10.com', '!5q%IYk0Hy')
        self.cria_pessoa('P1', 1)
        self.fazer_solicitacao('S1')
        # [To-Do] : Terminar o roteiro de testes...

if __name__ == '__main__':
    simulador = Simulador(
        Faker('pt_BR')
    )
    simulador.run()
