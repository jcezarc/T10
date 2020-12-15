import json
from flask_restful import Resource
from flask import request, jsonify

from flask_jwt_extended import jwt_required
from service.Evento_service import EventoService

class AllEvento(Resource):

    @jwt_required
    def get(self):
        """
        Returns all records from the table Evento

        #Read
        """
        service = EventoService()
        return service.find(request.args)
    
    @jwt_required
    def post(self):
        """
        Write a new record in Evento

        #Write
        """
        req_data = request.get_json()
        service = EventoService()
        return service.insert(req_data)

    @jwt_required
    def put(self):
        """
        Updates a record in Evento

        #Write
        """
        req_data = json.loads(request.data.decode("utf8"))
        service = EventoService()
        return service.update(req_data)
