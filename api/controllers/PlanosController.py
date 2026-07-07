import os
from repositories.PlanosRepository import PlanosRepository
from config.funcoes import success_response, exception_response


class PlanosController:
    def __init__(self, db):
        self.repository = PlanosRepository(db)

    def create_planos(self, data):
        try:
            return success_response(self.repository.create_planos(data), "Plano cadastrado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_planos(self, plano_id, data):
        try:
            return success_response(self.repository.update_planos(plano_id,data), "Plano alterado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_planos(self, plano_id):
        try:
            return success_response(self.repository.delete_planos(plano_id), "Plano deletado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_planos(self, plano_id, ativa):
        try:
            mensagem = "Plano desativado com sucesso"
            if ativa == 1:
                mensagem = "Plano ativado com sucesso"

            return success_response(self.repository.sfdelete_planos(plano_id, ativa), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)