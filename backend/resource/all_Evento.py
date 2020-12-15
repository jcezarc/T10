import json
from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required
)
from service.Evento_service import EventoService
from resource.user_controller import decode_user

class AllEvento(Resource):

    @staticmethod
    def current_user():
        """
        Obtém os dados do usuário autenticado
        """
        return decode_user(get_jwt_identity())

    @jwt_required
    def get(self):
        """
        Returns all records from the table Evento

        #Read
        """
        service = EventoService()
        return service.find(
            self.current_user()
        )

    @jwt_required
    def post(self):
        """
        Write a new record in Evento

        #Write
        """
        req_data = request.get_json()
        user = self.current_user()
        service = EventoService()
        return service.insert(req_data, user)
