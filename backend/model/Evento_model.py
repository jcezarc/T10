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
    NIVEL_SOLICITAR: 'Fazer solicitação',
    NIVEL_APROVACAO: 'Aprovar',
    NIVEL_REJEITAR: 'Rejeitar',
    NIVEL_CANCELAR: 'Cancelar',
}


class EventoModel(Schema):
    id = Str(primary_key=True, default="000", required=True)
    dt_evento = Date(default=datetime.today())
    situacao = Integer()
    solicitacao = Nested(SolicitacaoModel)
    usuario = Nested(PessoaModel)
