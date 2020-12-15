import json
from flask_restful import Resource
from flask import request, jsonify

from flask_jwt_extended import jwt_required
from service.Solicitacao_service import SolicitacaoService

class AllSolicitacao(Resource):

    @jwt_required
    def get(self):
        """
        Returns all records from the table Solicitacao

        #Read
        """
        service = SolicitacaoService()
        return service.find(request.args)
    
    @jwt_required
    def post(self):
        """
        Write a new record in Solicitacao

        #Write
        """
        req_data = request.get_json()
        service = SolicitacaoService()
        return service.insert(req_data)

    @jwt_required
    def put(self):
        """
        Updates a record in Solicitacao

        #Write
        """
        req_data = json.loads(request.data.decode("utf8"))
        service = SolicitacaoService()
        return service.update(req_data)
