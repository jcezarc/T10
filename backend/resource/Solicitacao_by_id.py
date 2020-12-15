from flask_restful import Resource

from flask_jwt_extended import jwt_required

from service.Solicitacao_service import SolicitacaoService

class SolicitacaoById(Resource):

    decorators=[jwt_required]

    @jwt_required
    def get(self, id):
        """
        Search in  Solicitacao by the field id

        #Read
        """
        service = SolicitacaoService()
        return service.find(None, id)

    @jwt_required
    def delete(self, id):
        """
        Delete a record of Solicitacao

        #Write
        """
        service = SolicitacaoService()
        return service.delete([id])
