import json
from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)
from service.Pessoa_service import PessoaService
from resource.user_controller import decode_user


class PessoaResource(Resource):

    @staticmethod
    def current_user():
        """
        Obtém os dados do usuário autenticado
        """
        return decode_user(get_jwt_identity())

    @jwt_required
    def get(self):
        """
        Traz uma lista de pessoas, que obedece
        os critérios passados na query
        Ex.: **.../T10/Pessoa?nome=Silva&nivel=3**

        #Consulta
        """
        service = PessoaService(user=self.current_user())
        return service.find(request.args)
    
    @jwt_required
    def post(self):
        """
        Grava uma nova Pessoa com nível
        inferior ao do usuário atual.

        #Gravação
        """
        req_data = request.get_json()
        service = PessoaService(user=self.current_user())
        return service.insert(req_data)
