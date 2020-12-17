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
from resource.Pessoa_resource import PessoaResource
from model.Evento_model import EventoModel
from resource.Evento_resource import EventoResource


BASE_PATH = '/T10'

def config_routes(app):
    api = Api(app)
    #--- Resources: ----
    api.add_resource(PessoaResource, f'{BASE_PATH}/Pessoa', methods=['GET'], endpoint='get_Pessoa')
    api.add_resource(PessoaResource, f'{BASE_PATH}/Pessoa', methods=['POST'], endpoint='post_Pessoa')
    api.add_resource(EventoResource, f'{BASE_PATH}/Evento', methods=['GET'], endpoint='get_Evento')
    api.add_resource(EventoResource, f'{BASE_PATH}/Evento', methods=['POST'], endpoint='post_Evento')   
    #-------------------

def set_swagger(app):
    swagger_url = '/docs'
    swaggerui_blueprint = get_swaggerui_blueprint(
        swagger_url,
        '/api',
        config={
            'app_name': "*- Defafio T10 -*"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)


def swagger_details(args):
    id_route = args[0]
    model = None
    resource = None
    docstring = ""
    if id_route == 'docs':
        docstring = """Documentação Swagger
        #Doc
        """
    elif id_route == 'Pessoa':
        resource = PessoaResource
        model = PessoaModel()
    elif id_route == 'Evento':
        resource = EventoResource
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


@APP.route(f'{BASE_PATH}/login', methods=['POST'])
def login():
    '''
    Gera um token para o usuário
    devidamente identificado

    #Acesso
    '''
    req_data = request.get_json()
    user = req_data.get('user')
    password = req_data.get('password')
    found = valid_user(user, password)
    if not found:
        return "Usuário inválido", 403
    access_token = create_access_token(identity=found)
    return jsonify(access_token=access_token), 200

if __name__ == '__main__':
    APP.run(debug=True)
