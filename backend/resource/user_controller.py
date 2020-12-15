import base64
import json
from service.Pessoa_service import PessoaService


CHAR_CODE = 'utf-8'


def encode_user(record):
    """
    Transforma dados de usuário
    p/ login numa string base64
    """
    return base64.b64encode(
        bytes(str(record), CHAR_CODE)
    ).decode(CHAR_CODE)

def decode_user(access_key):
    """
    Retorna dados de usuário
    associados à access_key
    """
    user_id = base64.b64decode(
        bytes(access_key, CHAR_CODE)
    ).decode(CHAR_CODE)
    return json.loads(
        user_id.replace("'", '"')
    )

def valid_user(user, password):
    service = PessoaService()
    msg, status_code = service.find({
        'email': user,
        'senha': password
    })
    if status_code == 404:
        return None
    data = msg['data']
    return encode_user(data)
