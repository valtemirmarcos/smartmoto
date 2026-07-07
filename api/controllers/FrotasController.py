import os
from repositories.FrotasRepository import FrotasRepository
from config.funcoes import success_response, exception_response


class FrotasController:
    def __init__(self, db):
        self.repository = FrotasRepository(db)

    def create_frotas(self, data, dados_token):
        try:
            return success_response(self.repository.create_frotas(data, dados_token), "Frota cadastrada com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_frotas(self, frota_id, data, dados_token):
        try:
            return success_response(self.repository.update_frotas(frota_id,data, dados_token), "Frota alterada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_frotas(self, frota_id):
        try:
            return success_response(self.repository.delete_frotas(frota_id), "Frota deletada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_frotas(self, frota_id, ativa, dados_token):
        try:
            mensagem = "Frota desativada com sucesso"
            if ativa == 1:
                mensagem = "Frota ativada com sucesso"

            return success_response(self.repository.sfdelete_frotas(frota_id, ativa, dados_token), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def listar_frotas(self, dados_token, filtros):
        try:
            return success_response(self.repository.listar_frotas(dados_token, filtros),"lista executada")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)