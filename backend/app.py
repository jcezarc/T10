# -*- coding: utf-8 -*-
import logging
from flask import Flask, Blueprint, request, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

import uuid
from flask_jwt_extended import create_access_token, JWTManager
from resource.user_controller import valid_user
from util.swagger_generator import FlaskSwaggerGenerator
from model.Pessoa_model import PessoaModel
from resource.Pessoa_by_id import PessoaById
from resource.all_Pessoa import AllPessoa
from model.Solicitacao_model import SolicitacaoModel
from resource.Solicitacao_by_id import SolicitacaoById
from resource.all_Solicitacao import AllSolicitacao
from model.Evento_model import EventoModel
from resource.Evento_by_id import EventoById
from resource.all_Evento import AllEvento


BASE_PATH = '/T10'

def config_routes(app):
    api = Api(app)
    #--- Resources: ----
    api.add_resource(PessoaById, f'{BASE_PATH}/Pessoa/<cpf_cnpj>', methods=['GET'], endpoint='get_Pessoa_by_id')
    api.add_resource(AllPessoa, f'{BASE_PATH}/Pessoa', methods=['GET'], endpoint='get_AllPessoa')
    api.add_resource(AllPessoa, f'{BASE_PATH}/Pessoa', methods=['POST'], endpoint='post_Pessoa')
    api.add_resource(AllPessoa, f'{BASE_PATH}/Pessoa', methods=['PUT'], endpoint='put_Pessoa')
    api.add_resource(PessoaById, f'{BASE_PATH}/Pessoa/<cpf_cnpj>', methods=['DELETE'], endpoint='delete_Pessoa')
    api.add_resource(SolicitacaoById, f'{BASE_PATH}/Solicitacao/<id>', methods=['GET'], endpoint='get_Solicitacao_by_id')
    api.add_resource(AllSolicitacao, f'{BASE_PATH}/Solicitacao', methods=['GET'], endpoint='get_AllSolicitacao')
    api.add_resource(AllSolicitacao, f'{BASE_PATH}/Solicitacao', methods=['POST'], endpoint='post_Solicitacao')
    api.add_resource(AllSolicitacao, f'{BASE_PATH}/Solicitacao', methods=['PUT'], endpoint='put_Solicitacao')
    api.add_resource(SolicitacaoById, f'{BASE_PATH}/Solicitacao/<id>', methods=['DELETE'], endpoint='delete_Solicitacao')
    api.add_resource(EventoById, f'{BASE_PATH}/Evento/<id>', methods=['GET'], endpoint='get_Evento_by_id')
    api.add_resource(AllEvento, f'{BASE_PATH}/Evento', methods=['GET'], endpoint='get_AllEvento')
    api.add_resource(AllEvento, f'{BASE_PATH}/Evento', methods=['POST'], endpoint='post_Evento')
    api.add_resource(AllEvento, f'{BASE_PATH}/Evento', methods=['PUT'], endpoint='put_Evento')
    api.add_resource(EventoById, f'{BASE_PATH}/Evento/<id>', methods=['DELETE'], endpoint='delete_Evento')
    
    #-------------------

def set_swagger(app):
    swagger_url = '/docs'
    swaggerui_blueprint = get_swaggerui_blueprint(
        swagger_url,
        '/api',
        config={
            'app_name': "*- T10 -*"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)


def swagger_details(args):
    id_route = args[0]
    params = args[1]
    model = None
    resource = None
    docstring = ""
    if id_route == 'docs':
        docstring = """Swagger documentation
        #Doc
        """
    elif id_route == 'Pessoa':
        if not params:
            resource = AllPessoa
        else:
            resource = PessoaById
        model = PessoaModel()
    elif id_route == 'Solicitacao':
        if not params:
            resource = AllSolicitacao
        else:
            resource = SolicitacaoById
        model = SolicitacaoModel()
    elif id_route == 'Evento':
        if not params:
            resource = AllEvento
        else:
            resource = EventoById
        model = EventoModel()
    
    ignore = False
    return model, resource, docstring, ignore

logging.basicConfig(
    filename='T10.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

APP = Flask(__name__)
CORS(APP)

APP.config['JWT_SECRET_KEY'] = str(uuid.uuid4())
JWT = JWTManager(APP)
config_routes(APP)
set_swagger(APP)

@APP.route('/api')
def get_api():
    """
    API json data

    #Doc
    """
    generator = FlaskSwaggerGenerator(
        swagger_details,
        None
    )
    return jsonify(generator.content)

@APP.route('/health')
def health():
    return 'OK', 200


@APP.route('/handshake', methods=['POST'])
def handshake():
    user = request.json.get('user')
    password = request.json.get('password')
    found, user_id = valid_user(user, password)
    if not found:
        return "Invalid user", 403
    access_token = create_access_token(identity=user_id)
    return jsonify(access_token=access_token), 200

if __name__ == '__main__':
    APP.run(debug=True)
