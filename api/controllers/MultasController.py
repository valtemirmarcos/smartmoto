import os
from repositories.MultasRepository import MultasRepository
from config.funcoes import success_response, exception_response


class MultasController:
    def __init__(self, db):
        self.repository = MultasRepository(db)

    def create_multas(self, data, dados_token):
        try:
            return success_response(self.repository.create_multas(data, dados_token), "Multa cadastrada com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_multas(self, multa_id, data, dados_token):
        try:
            return success_response(self.repository.update_multas(multa_id,data, dados_token), "Multa alterada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_multas(self, multa_id):
        try:
            return success_response(self.repository.delete_multas(multa_id), "Multa deletada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_multas(self, multa_id, ativa, dados_token):
        try:
            mensagem = "Multa desativada com sucesso"
            if ativa == 1:
                mensagem = "Multa ativada com sucesso"

            return success_response(self.repository.sfdelete_multas(multa_id, ativa, dados_token), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def listar_multas(self, dados_token, filtros):
        try:
            return success_response(self.repository.listar_multas(dados_token, filtros), "Multas listadas com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)