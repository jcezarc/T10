from marshmallow import Schema
from marshmallow.fields import Str, Nested, List, Integer, Float, Date, Boolean


PK_DEFAULT_VALUE = "000"

class PessoaModel(Schema):
    cpf_cnpj = Str(primary_key=True, default=PK_DEFAULT_VALUE, required=True)
    nome = Str()
    email = Str(required=True)
    senha = Str(required=True)
    nivel = Integer()
