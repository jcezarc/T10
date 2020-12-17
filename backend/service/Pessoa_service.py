import logging
from model.Pessoa_model import PessoaModel
from util.messages import (
    resp_error,
    resp_not_found,
    resp_post_ok,
    resp_get_ok,
    resp_ok
)
from service.db_connection import get_table

class PessoaService:
    def __init__(self, table=None, user=None):
        if table:
            self.table = table
        else:
            self.table = get_table(PessoaModel)
        self.user = user

    def find(self, params):
        logging.info('Procurando Pessoas...')
        found = self.table.find_all(
            20,
            self.table.get_conditions(params, False)
        )
        if not found:
            return resp_not_found()
        return resp_get_ok(found)


    def insert(self, json_data):
        logging.info('Gravando nova Pessoa')
        user = self.user
        def get_level(record):
            return int(record.get('nivel', 1))
        if get_level(json_data) > get_level(user):
            return resp_error('Você não pode criar um usuário com nível maior que o seu.')
        errors = self.table.insert(json_data)
        if errors:
            return resp_error(errors)
        return resp_post_ok(json_data)
