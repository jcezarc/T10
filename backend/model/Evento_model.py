import uuid
from marshmallow import Schema
from marshmallow.fields import Str, Nested, List, Integer, Float, Date, Boolean
from model.Solicitacao_model import SolicitacaoModel
from model.Pessoa_model import PessoaModel
from datetime import datetime


NIVEL_SOLICITAR = 1
NIVEL_APROVACAO = 2
NIVEL_REJEITAR = 3
NIVEL_CANCELAR = 4

NOME_SITUACAO = {
    NIVEL_SOLICITAR: 'Solicita',
    NIVEL_APROVACAO: 'Aprova',
    NIVEL_REJEITAR: 'Rejeita',
    NIVEL_CANCELAR: 'Cancela',
}


class EventoModel(Schema):
    id = Str(
        primary_key=True,
        default=str(uuid.uuid4()),
        required=True
    )
    dt_evento = Date(default=datetime.today())
    situacao = Integer(default=1)
    solicitacao = Nested(SolicitacaoModel)
    usuario = Nested(PessoaModel)
