'''
Executa os testes funcionais da API,
cumprindo um roteiro de chamadas e
avaliando o retorno de cada uma delas.
'''

import requests
from faker import Faker

EV_SOLICITAR = 1
EV_APROVACAO = 2
EV_REJEITAR = 3
EV_CANCELAR = 4
BASE_URL = 'http://localhost/T10/{}'
SENHA_DEFAULT = 'xyz123'


class Simulador:

    def __init__(self, faker):
        self.faker = faker
        self.token = None
        self.pessoa = None

    def login(self, usuario, senha=SENHA_DEFAULT):
        self.pessoa = usuario
        print('\t>> Login: ', usuario)
        dados = {}
        dados['usuario'] = usuario
        dados['senha'] = senha
        url = BASE_URL.format('login')
        resp = requests.post(url, json=dados)
        assert resp.status_code == 200
        self.token = resp.text

    def autenticacao(self):
        return {
            'Authorization': 'Bearer {}'.format(self.token)
        }

    def cria_pessoa(self, id, nivel):
        dados = {}
        fake = self.faker
        print('-'*50)
        print('[POST]', id)
        dados['cpf_cnpj'] = id
        dados['nome'] = fake.name()
        dados['email'] = fake.email()
        dados['nivel'] = nivel
        dados['senha'] = fake.password()
        resp = requests.post(
            BASE_URL.format('Pessoa'),
            json=dados,
            header=self.autenticacao()
        )
        assert resp.status_code == 201

    def dispara_evento(self, situacao, solicitacao, pessoa, esperado):
        dados = {}
        print('-'*50)
        print('[POST]', solicitacao)
        if situacao == EV_SOLICITAR:
            fake = self.faker
            solicitacao = {
                'id': solicitacao,
                'conta': fake.credit_card_number(),
                'detalhes': fake.text(200)
            }
        if self.pessoa != pessoa:
            self.login(pessoa)
        dados['situacao'] = situacao
        dados['solicitacao'] = solicitacao
        resp = requests.post(
            BASE_URL.format('Evento'),
            json=dados,
            header=self.autenticacao()
        )
        status_code = resp.status_code
        assert status_code == esperado

    def run(self):
        print('\n*** Testes funcionais para o desafio T10 ***')
        self.login('admin@desafio-t10.com', '!5q%IYk0Hy')
        self.cria_pessoa('P1', 1)
        self.cria_pessoa('P2', 3)
        self.cria_pessoa('P3', 4)
        self.dispara_evento(EV_SOLICITAR, 'S1', 'P1', 201)
        self.dispara_evento(EV_APROVACAO, 'S1', 'P1', 400)
        self.dispara_evento(EV_REJEITAR, 'S1', 'P2', 201)
        self.dispara_evento(EV_SOLICITAR, 'S3', 'P1', 201)
        self.dispara_evento(EV_APROVACAO, 'S3', 'P2', 201)
        


if __name__ == '__main__':
    simulador = Simulador(
        Faker('pt_BR')
    )
    simulador.run()
