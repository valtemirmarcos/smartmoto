import os
from repositories.CalcoesRepository import CalcoesRepository
from config.funcoes import success_response, exception_response


class CalcoesController:
    def __init__(self, db):
        self.repository = CalcoesRepository(db)

    def create_calcoes(self, data, dados_token):
        try:
            return success_response(self.repository.create_calcoes(data, dados_token), "Calção cadastrado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_calcoes(self, calcao_id, data, dados_token):
        try:
            return success_response(self.repository.update_calcoes(calcao_id,data, dados_token), "Calção alterado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_calcoes(self, calcao_id):
        try:
            return success_response(self.repository.delete_calcoes(calcao_id), "Calção deletado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_calcoes(self, calcao_id, ativa, dados_token):
        try:
            mensagem = "Calção desativado com sucesso"
            if ativa == 1:
                mensagem = "Calção ativado com sucesso"

            return success_response(self.repository.sfdelete_calcoes(calcao_id, ativa, dados_token), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def listar_calcoes(self, dados_token, filtro):
        try:
            return success_response(self.repository.listar_calcoes(dados_token, filtro), "Calções listados com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)