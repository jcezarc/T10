import sys
sys.path.append('..')
from service.Pessoa_service import PessoaService
from model.Pessoa_model import PessoaModel
from util.db.lite_table import LiteTable
from util.tester import Tester


def get_service(user):
    table = LiteTable(
        PessoaModel, {
             'database': ':memory:'
        }
    )
    table.create_table()
    return PessoaService(table, user)

def test_find_success():
    test = Tester(get_service)
    test.find_success()

def test_find_failure():
    test = Tester(get_service)
    test.find_failure()

def test_insert_success():
    test = Tester(get_service)
    test.insert_success()

def test_insert_failure():
    test = Tester(get_service)
    test.insert_failure()
