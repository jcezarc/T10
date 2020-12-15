from flask_restful import Resource

from flask_jwt_extended import jwt_required

from service.Pessoa_service import PessoaService

class PessoaById(Resource):

    decorators=[jwt_required]

    @jwt_required
    def get(self, cpf_cnpj):
        """
        Search in  Pessoa by the field cpf_cnpj

        #Read
        """
        service = PessoaService()
        return service.find(None, cpf_cnpj)

    @jwt_required
    def delete(self, cpf_cnpj):
        """
        Delete a record of Pessoa

        #Write
        """
        service = PessoaService()
        return service.delete([cpf_cnpj])
