from flask_restful import Resource

from flask_jwt_extended import jwt_required

from service.Evento_service import EventoService

class EventoById(Resource):

    decorators=[jwt_required]

    @jwt_required
    def get(self, id):
        """
        Search in  Evento by the field id

        #Read
        """
        service = EventoService()
        return service.find(None, id)

    @jwt_required
    def delete(self, id):
        """
        Delete a record of Evento

        #Write
        """
        service = EventoService()
        return service.delete([id])
