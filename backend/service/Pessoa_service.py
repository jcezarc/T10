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
    def __init__(self, table=None):
        if table:
            self.table = table
        else:
            self.table = get_table(PessoaModel)

    def find(self, params, cpf_cnpj=None):
        if cpf_cnpj is None:
            logging.info('Finding all records of Pessoa...')
            found = self.table.find_all(
                20,
                self.table.get_conditions(params, False)
            )
        else:
            logging.info(f'Finding "{cpf_cnpj}" in Pessoa ...')
            found = self.table.find_one([cpf_cnpj])
        if not found:
            return resp_not_found()
        return resp_get_ok(found)


    def insert(self, json_data, user):
        logging.info('Gravando nova Pessoa')

        def get_level(record):
            return record.get('nivel', 1)
        if get_level(json_data) > get_level(user):
            return resp_error('Você não pode criar um usuário com nível maior que o seu.')
        errors = self.table.insert(json_data)
        if errors:
            return resp_error(errors)
        return resp_post_ok()
