import os
from repositories.PlanosRepository import PlanosRepository
from config.funcoes import success_response, exception_response


class PlanosController:
    def __init__(self, db):
        self.repository = PlanosRepository(db)

    def create_planos(self, data, dados_token):
        try:
            return success_response(self.repository.create_planos(data, dados_token), "Plano cadastrado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_planos(self, plano_id, data, dados_token):
        try:
            return success_response(self.repository.update_planos(plano_id, data, dados_token), "Plano alterado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_planos(self, plano_id, dados_token):
        try:
            return success_response(self.repository.delete_planos(plano_id, dados_token), "Plano deletado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_planos(self, plano_id, ativa, dados_token):
        try:
            mensagem = "Plano desativado com sucesso"
            if ativa == 1:
                mensagem = "Plano ativado com sucesso"

            return success_response(self.repository.sfdelete_planos(plano_id, ativa, dados_token), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def listar_planos(self, dados_token, filtros):
        try:
            return success_response(self.repository.listar_planos(dados_token, filtros), "Planos listados com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)