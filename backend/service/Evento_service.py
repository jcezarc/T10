import logging
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
    def __init__(self, table=None):
        if table:
            self.table = table
        else:
            self.table = get_table(EventoModel)

    def find(self, user):
        logging.info('Procurando por Eventos...')
        '''
        Procura eventos do usuario ou com nível abaixo dele
        '''
        found = self.table.find_all(
            20,
            'usuario = "{}" OR situacao < {}'.format(
                user['cpf_cnpf'],
                user['nivel']
            )
        )
        if not found:
            return resp_not_found()
        return resp_get_ok(found)

    def insert(self, json_data, user):
        logging.info('New record write in Evento')
        errors = self.table.insert(json_data)
        if errors:
            return resp_error(errors)
        new_level = int(json_data.get('situacao', 1))
        cur_level = int(user['nivel'])
        if new_level > cur_level:
            return resp_error('Você não tem permissão para {}'.format(
                NOME_SITUACAO[new_level]
            ))
        solicitacao = json_data.get('solicitacao')
        if new_level == NIVEL_SOLICITAR and isinstance(solicitacao, dict):
            # --- No evento de fazer solicitação, grava os detalhes na tabela Solicitacao
            service = SolicitacaoService()
            service.insert(solicitacao)
        return resp_post_ok()
