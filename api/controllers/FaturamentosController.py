import os
from repositories.FaturamentosRepository import FaturamentosRepository
from config.funcoes import success_response, exception_response


class FaturamentosController:
    def __init__(self, db):
        self.repository = FaturamentosRepository(db)

    def create_faturamentos(self, data, dados_token):
        try:
            return success_response(self.repository.create_faturamentos(data, dados_token), "Faturamento cadastrado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_faturamentos(self, faturamento_id, data, dados_token):
        try:
            return success_response(self.repository.update_faturamentos(faturamento_id,data, dados_token), "Faturamento alterado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_faturamentos(self, faturamento_id):
        try:
            return success_response(self.repository.delete_faturamentos(faturamento_id), "Faturamento deletado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_faturamentos(self, faturamento_id, ativa, dados_token):
        try:
            mensagem = "Faturamento desativado com sucesso"
            if ativa == 1:
                mensagem = "Faturamento ativado com sucesso"

            return success_response(self.repository.sfdelete_faturamentos(faturamento_id, ativa, dados_token), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def gerarFatura(self, franquiado_id, mes, ano, dados_token, royaties=None):
        try:
            return success_response(self.repository.gerarFatura(franquiado_id, mes, ano, dados_token, royaties), "Faturamento gerado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def listar_faturamentos(self, dados_token, filtros_url):
        try:
            return success_response(self.repository.listar_faturamentos(dados_token, filtros_url), "Faturamentos listados com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)