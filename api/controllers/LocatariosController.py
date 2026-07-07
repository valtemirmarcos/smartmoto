import os
from repositories.LocatariosRepository import LocatariosRepository
from config.funcoes import success_response, exception_response


class LocatariosController:
    def __init__(self, db):
        self.repository = LocatariosRepository(db)

    def listar_locatarios(self, dados_token, filtros_url):
        try:
            return success_response(self.repository.listar_locatarios(dados_token, filtros_url), "Locatarios listado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)