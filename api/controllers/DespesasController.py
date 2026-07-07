import os
from repositories.DespesasRepository import DespesasRepository
from config.funcoes import success_response, exception_response


class DespesasController:
    def __init__(self, db):
        self.repository = DespesasRepository(db)

    def create_despesas(self, data, dados_token):
        try:
            return success_response(self.repository.create_despesas(data, dados_token), "Despesa cadastrada com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_despesas(self, despesa_id, data, dados_token):
        try:
            return success_response(self.repository.update_despesas(despesa_id,data, dados_token), "Despesa alterada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_despesas(self, despesa_id):
        try:
            return success_response(self.repository.delete_despesas(despesa_id), "Despesa deletada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_despesas(self, despesa_id, ativa, dados_token):
        try:
            mensagem = "Despesa desativada com sucesso"
            if ativa == 1:
                mensagem = "Despesa ativada com sucesso"

            return success_response(self.repository.sfdelete_despesas(despesa_id, ativa, dados_token), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def listar_despesas(self, dados_token, filtro):
        try:
            return success_response(self.repository.listar_despesas(dados_token, filtro), "Despesa deletada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)