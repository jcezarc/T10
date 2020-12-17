import uuid
import logging
from datetime import datetime
from model.Evento_model import EventoModel, NOME_SITUACAO, NIVEL_SOLICITAR
from util.messages import (
    resp_error,
    resp_not_found,
    resp_post_ok,
    resp_get_ok,
    resp_ok
)
from service.db_connection import get_table
from service.Solicitacao_service import SolicitacaoService


class EventoService:

    def __init__(self, table=None, user=None):
        if table:
            self.table = table
        else:
            self.table = get_table(EventoModel)
        self.user = user

    @staticmethod
    def substitui_nome_sit(dados):
        '''
        Coloca os nomes das situações
        em vez dos códigos numéricos
        '''
        for item in dados:
            situacao = int(item['situacao'])
            item['situacao'] = '{}do'.format(
                NOME_SITUACAO[situacao]
            )

    def find(self, params):
        user = self.user
        logging.info('Procurando por Eventos...')
        '''
        Procura eventos do usuario ou com nível abaixo dele
        '''
        found = self.table.find_all(
            20,
            "usuario = '{}' OR situacao < {}".format(
                user['cpf_cnpj'],
                user['nivel']
            ),
            allow_left_joins=False
        )
        if not found:
            return resp_not_found()
        self.substitui_nome_sit(found)
        return resp_get_ok(found)

    def insert(self, json_data):
        user = self.user
        logging.info('Gravando novo Evento')
        new_level = int(json_data.get('situacao', 1))
        cur_level = int(user['nivel'])
        if new_level > cur_level:
            return resp_error('Você não tem permissão para {}r'.format(
                NOME_SITUACAO[new_level]
            ))
        solicitacao = json_data.get('solicitacao')
        if new_level > NIVEL_SOLICITAR:
            found = self.table.find_all(
                1,
                f"solicitacao = '{solicitacao}'",
                allow_left_joins=False
            )
            if not found:
                return resp_error(
                    'Não existe nada para {}r'.format(
                        NOME_SITUACAO[new_level]
                    )
                )
        elif isinstance(solicitacao, dict):
            # --- No evento de fazer solicitação, grava os detalhes na tabela Solicitacao
            service = SolicitacaoService()
            msg, status_code = service.insert(solicitacao)
            if status_code == 400:
                return msg, status_code
        json_data['usuario'] = user['cpf_cnpj']
        json_data['id'] = str(uuid.uuid4())
        today = datetime.today()
        json_data['dt_evento'] = today.strftime('%Y-%m-%d')
        errors = self.table.insert(json_data)
        if errors:
            print('='*100)
            print(json_data)
            print('-'*100)
            print('Erros:')
            print(errors)
            return resp_error(errors)
        return resp_post_ok(json_data)
