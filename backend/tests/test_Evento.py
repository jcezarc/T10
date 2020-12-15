import sys
sys.path.append('..')
from service.Evento_service import EventoService
from model.Evento_model import EventoModel, PK_DEFAULT_VALUE
from util.db.fake_table import FakeTable
from util.messages import resp_ok, resp_not_found

def test_find_success():
    table = FakeTable(EventoModel)
    record = table.default_values()
    table.insert(record)
    service = EventoService(table)
    status_code = service.find(None, PK_DEFAULT_VALUE)[1]
    assert status_code == 200

def test_find_failure():
    service = EventoService(FakeTable(EventoModel))
    status_code = service.find(None, PK_DEFAULT_VALUE)[1]
    assert status_code == 404

def test_insert_success():
    table = FakeTable(EventoModel)
    service = EventoService(table)
    record = table.default_values()
    status_code = service.insert(record)[1]
    assert status_code == 201

def test_insert_failure():
    service = EventoService(FakeTable(EventoModel))
    status_code = service.insert({})[1]
    assert status_code == 400
