import os
from repositories.FranquiasRepository import FranquiasRepository
from config.funcoes import success_response, exception_response


class FranquiasController:
    def __init__(self, db):
        self.repository = FranquiasRepository(db)

    def create_franquias(self, data):
        try:
            return success_response(self.repository.create_franquias(data))
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_franquias(self, franquia_id, data):
        try:
            return success_response(self.repository.update_franquias(franquia_id,data), "Franquia alterada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_franquias(self, franquia_id):
        try:
            return success_response(self.repository.delete_franquias(franquia_id), "Franquia deletada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_franquias(self, franquia_id, ativa):
        try:
            mensagem = "Franquia desativada com sucesso"
            if ativa == 1:
                mensagem = "Franquia ativada com sucesso"

            return success_response(self.repository.sfdelete_franquias(franquia_id, ativa), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)