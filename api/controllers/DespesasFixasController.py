import os
from repositories.DespesasFixasRepository import DespesasFixasRepository
from config.funcoes import success_response, exception_response


class DespesasFixasController:
    def __init__(self, db):
        self.repository = DespesasFixasRepository(db)

    def create_despesas_fixas(self, data, dados_token):
        try:
            return success_response(self.repository.create_despesas_fixas(data, dados_token), "Despesa cadastrada com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_despesas_fixas(self, df_id, data, dados_token):
        try:
            return success_response(self.repository.update_despesas_fixas(df_id,data, dados_token), "Despesa alterada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_despesas_fixas(self, df_id, dados_token):
        try:
            return success_response(self.repository.delete_despesas_fixas(df_id, dados_token), "Despesa deletada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_despesas_fixas(self, df_id, ativa, dados_token):
        try:
            mensagem = "Despesa desativada com sucesso"
            if ativa == 1:
                mensagem = "Despesa ativada com sucesso"

            return success_response(self.repository.sfdelete_despesas_fixas(df_id, ativa, dados_token), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def listar_despesas_fixas(self, dados_token, filtro):
        try:
            return success_response(self.repository.listar_despesas_fixas(dados_token, filtro), "Despesas fixas listadas com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)