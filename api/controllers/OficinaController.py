import os
from repositories.OficinaRepository import OficinaRepository
from config.funcoes import success_response, exception_response


class OficinaController:
    def __init__(self, db):
        self.repository = OficinaRepository(db)

    def create_oficina(self, data, dados_token):
        try:
            return success_response(self.repository.create_oficina(data, dados_token), "Serviço de Oficina  cadastrado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_oficina(self, oficina_id, data, dados_token):
        try:
            return success_response(self.repository.update_oficina(oficina_id,data, dados_token), "Serviço de Oficina  alterado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_oficina(self, oficina_id):
        try:
            return success_response(self.repository.delete_oficina(oficina_id), "Serviço de Oficina deletado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_oficina(self, oficina_id, ativa, dados_token):
        try:
            mensagem = "Serviço de Oficina desativado com sucesso"
            if ativa == 1:
                mensagem = "Serviço de Oficina ativado com sucesso"

            return success_response(self.repository.sfdelete_oficina(oficina_id, ativa, dados_token), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def listar_oficina(self, dados_token, filtro):
        try:
            return success_response(self.repository.listar_oficina(dados_token, filtro), "Serviços de Oficina listados com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)