import sys
sys.path.append('..')
from service.Solicitacao_service import SolicitacaoService
from model.Solicitacao_model import SolicitacaoModel, PK_DEFAULT_VALUE
from util.db.lite_table import LiteTable
from util.tester import Tester


def get_service():
    table = LiteTable(
        SolicitacaoModel, {
             'database': ':memory:'
        }
    )
    table.create_table()
    return SolicitacaoService(table)

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
