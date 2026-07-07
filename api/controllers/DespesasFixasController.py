import os
from repositories.DespesasFixasRepository import DespesasFixasRepository
from config.funcoes import success_response, exception_response


class DespesasFixasController:
    def __init__(self, db):
        self.repository = DespesasFixasRepository(db)

    def create_despesas_fixas(self, data):
        try:
            return success_response(self.repository.create_despesas_fixas(data), "Despesa cadastrada com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_despesas_fixas(self, df_id, data):
        try:
            return success_response(self.repository.update_despesas_fixas(df_id,data), "Despesa alterada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_despesas_fixas(self, df_id):
        try:
            return success_response(self.repository.delete_despesas_fixas(df_id), "Despesa deletada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_despesas_fixas(self, df_id, ativa):
        try:
            mensagem = "Despesa desativada com sucesso"
            if ativa == 1:
                mensagem = "Despesa ativada com sucesso"

            return success_response(self.repository.sfdelete_despesas_fixas(df_id, ativa), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)