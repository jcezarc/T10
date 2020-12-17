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
BASE_URL = 'http://localhost:5000/T10/{}'
SENHA_DEFAULT = 'xyz123'
NOME_SITUACAO = {
    EV_SOLICITAR: 'Solicitar',
    EV_APROVACAO: 'Aprovar',
    EV_REJEITAR: 'Rejeitar',
    EV_CANCELAR: 'Cancelar',
}



class Simulador:

    def __init__(self, faker):
        self.faker = faker
        self.token = None
        self.pessoa = None
        self.line = 0

    def login(self, usuario, senha=SENHA_DEFAULT):
        self.pessoa = usuario
        print('\t>> Login: ', usuario)
        dados = {}
        dados['user'] = usuario
        dados['password'] = senha
        url = BASE_URL.format('login')
        resp = requests.post(url, json=dados)
        assert resp.status_code == 200
        self.token = resp.json()['access_token']

    def autenticacao(self):
        return {
            'Authorization': 'Bearer {}'.format(self.token)
        }

    def cria_pessoa(self, id, nivel, esperado=201):
        self.line += 1
        dados = {}
        fake = self.faker
        print('-'*50)
        print(self.line, '[POST] Pessoa:', id)
        dados['cpf_cnpj'] = id
        dados['nome'] = fake.name()
        dados['email'] = id
        dados['nivel'] = nivel
        dados['senha'] = SENHA_DEFAULT
        resp = requests.post(
            BASE_URL.format('Pessoa'),
            json=dados,
            headers=self.autenticacao()
        )
        assert resp.status_code == esperado

    def dispara_evento(self, situacao, solicitacao, pessoa, esperado=201):
        self.line += 1
        dados = {}
        print('-'*50)
        print('{} [POST] {} {}'.format(
            self.line,
            NOME_SITUACAO[situacao],
            solicitacao,
        ))
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
            headers=self.autenticacao()
        )
        status_code = resp.status_code
        if status_code != esperado:
            print('@'*50)
            print(resp.json())
        assert status_code == esperado

    def faz_consulta(self, pessoa, esperado):
        self.line += 1
        print('-'*50)
        print(self.line, '[GET] Evento')
        if self.pessoa != pessoa:
            self.login(pessoa)

        def existe_solicitacao(id, dados):
            for item in dados:
                solicitacao = item['solicitacao'].replace(' ', '')
                if solicitacao == id:
                    return True
            return False
        resp = requests.get(
            BASE_URL.format('Evento'),
            headers=self.autenticacao()
        )
        assert resp.status_code == 200
        dados = resp.json()['data']
        while esperado:
            id = esperado.pop(0)
            assert existe_solicitacao(id, dados)

    def run(self):
        print('\n*** Testes funcionais para o desafio T10 ***')
        self.login('admin@desafio-t10.com', '!5q%IYk0Hy')
        # 1
        self.cria_pessoa('P1', EV_SOLICITAR)
        # 2
        self.cria_pessoa('P2', EV_REJEITAR)
        # 3
        self.cria_pessoa('P3', EV_CANCELAR)
        # 4
        self.dispara_evento(EV_SOLICITAR, 'S1', 'P1')
        # 5
        self.dispara_evento(EV_APROVACAO, 'S1', 'P1', 400)
        # 6
        self.dispara_evento(EV_REJEITAR, 'S1', 'P2')
        # 7
        self.dispara_evento(EV_SOLICITAR, 'S2', 'P1')
        # 8
        self.faz_consulta('P1', ['S1', 'S2'])
        # 9
        self.dispara_evento(EV_APROVACAO, 'S2', 'P2')
        # 10
        self.login('P2')
        self.cria_pessoa('P4', 4, 400)
        # 11
        self.dispara_evento(EV_CANCELAR, 'S2', 'P3')
        # 12
        self.dispara_evento(EV_APROVACAO, 'S3', 'P2', 400)
        # 13
        self.dispara_evento(EV_SOLICITAR, 'S3', 'P2')
        # 14
        self.faz_consulta('P1', ['S1', 'S2'])
        # 15
        self.faz_consulta('P3', ['S1', 'S2', 'S3'])
        # ---------------
        print('\n* * *  Teste concluído com sucesso!!!  * * * \n')


if __name__ == '__main__':
    simulador = Simulador(
        Faker('pt_BR')
    )
    simulador.run()
