import json
from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)
from service.Evento_service import EventoService
from resource.user_controller import decode_user

class EventoResource(Resource):

    @staticmethod
    def current_user():
        """
        Obtém os dados do usuário autenticado
        """
        return decode_user(get_jwt_identity())

    @jwt_required
    def get(self):
        """
        Retorna todos os eventos que
        o usuário atual tem acesso

        #Consulta
        """
        service = EventoService(user=self.current_user())
        return service.find(None)

    @jwt_required
    def post(self):
        """
        Grava um novo Evento
        `Regras`: 
        - O usuário só pode
        gravar eventos permitidos para o
        seu nível;
        - Aprovar, rejeitar e cancelar somente
        são possíveis para solicitações já
        efetuadas.
        
        #Gravação
        """
        req_data = request.get_json()
        service = EventoService(user=self.current_user())
        return service.insert(req_data)
