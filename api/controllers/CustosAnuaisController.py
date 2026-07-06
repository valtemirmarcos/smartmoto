import os
from repositories.CustosAnuaisRepository import CustosAnuaisRepository
from config.funcoes import success_response, exception_response


class CustosAnuaisController:
    def __init__(self, db):
        self.repository = CustosAnuaisRepository(db)

    def create_custos_anuais(self, data, dados_token):
        try:
            return success_response(self.repository.create_custos_anuais(data, dados_token), "Custo cadastrado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_custos_anuais(self, custo_anual_id, data, dados_token):
        try:
            return success_response(self.repository.update_custos_anuais(custo_anual_id,data, dados_token), "Custo alterado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_custos_anuais(self, custo_anual_id):
        try:
            return success_response(self.repository.delete_custos_anuais(custo_anual_id), "Custo deletado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_custos_anuais(self, custo_anual_id, ativa, dados_token):
        try:
            mensagem = "Custo desativada com sucesso"
            if ativa == 1:
                mensagem = "Custo ativada com sucesso"

            return success_response(self.repository.sfdelete_custos_anuais(custo_anual_id, ativa, dados_token), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def listar_custos_anuais(self, dados_token, filtro):
        try:
            return success_response(self.repository.listar_custos_anuais(dados_token, filtro), "Custo listados com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)