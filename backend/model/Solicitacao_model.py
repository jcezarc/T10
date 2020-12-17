from marshmallow import Schema
from marshmallow.fields import Str, Nested, List, Integer, Float, Date, Boolean


class SolicitacaoModel(Schema):
    id = Str(primary_key=True, required=True)
    conta = Str()
    detalhes = Str()
