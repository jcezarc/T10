import json
from flask_restful import Resource
from flask import request, jsonify

from flask_jwt_extended import jwt_required
from service.Pessoa_service import PessoaService

class PessoaResource(Resource):

    @jwt_required
    def get(self):
        """
        Traz uma lista de pessoas, que obedece
        os critérios passados na query
        Ex.: **.../T10/Pessoa?nome=Silva&nivel=3**

        #Consulta
        """
        service = PessoaService()
        return service.find(request.args)
    
    @jwt_required
    def post(self):
        """
        Grava uma nova Pessoa com nível
        inferior ao do usuário atual.

        #Gravação
        """
        req_data = request.get_json()
        service = PessoaService()
        return service.insert(req_data)
