import sys
sys.path.append('..')
from service.Evento_service import EventoService
from model.Evento_model import EventoModel
from util.db.lite_table import LiteTable
from util.tester import Tester


def get_service(user):
    table = LiteTable(
        EventoModel, {
            'database': Tester.temp_file()
            #  'database': ':memory:'
        }
    )
    table.create_table()
    return EventoService(table, user)

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
