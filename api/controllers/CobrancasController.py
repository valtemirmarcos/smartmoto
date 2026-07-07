import os
from repositories.CobrancasRepository import CobrancasRepository
from config.funcoes import success_response, exception_response


class CobrancasController:
    def __init__(self, db):
        self.repository = CobrancasRepository(db)

    def create_cobrancas(self, data):
        try:
            return success_response(self.repository.create_cobrancas(data), "Cobrança cadastrada com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_cobrancas(self, cobranca_id, data):
        try:
            return success_response(self.repository.update_cobrancas(cobranca_id,data), "Cobrança alterada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_cobrancas(self, cobranca_id):
        try:
            return success_response(self.repository.delete_cobrancas(cobranca_id), "Cobrança deletada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_cobrancas(self, cobranca_id, ativa):
        try:
            mensagem = "Cobrança desativada com sucesso"
            if ativa == 1:
                mensagem = "Cobrança ativada com sucesso"

            return success_response(self.repository.sfdelete_cobrancas(cobranca_id, ativa), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)