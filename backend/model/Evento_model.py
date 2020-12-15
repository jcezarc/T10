from marshmallow import Schema
from marshmallow.fields import Str, Nested, List, Integer, Float, Date, Boolean
from model.Solicitacao_model import SolicitacaoModel
from model.Pessoa_model import PessoaModel


PK_DEFAULT_VALUE = "000"

class EventoModel(Schema):
    id = Str(primary_key=True, default=PK_DEFAULT_VALUE, required=True)
    dt_evento = Date()
    situacao = Integer()

    solicitacao = Nested(SolicitacaoModel)
    usuario = Nested(PessoaModel)

