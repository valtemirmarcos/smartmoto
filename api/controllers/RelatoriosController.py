import os
from repositories.RelatoriosRepository import RelatoriosRepository
from config.funcoes import success_response, exception_response


class RelatoriosController:
    def __init__(self, db):
        self.repository = RelatoriosRepository(db)


    def dashboard(self, dados_token, filtros):
        try:
            return success_response(self.repository.dashboard(dados_token, filtros), "Dashboard listada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def custos(self, dados_token, filtros):
        try:
            return success_response(self.repository.custos(dados_token, filtros), "Custos listada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)
    
    def custo_moto(self, dados_token, filtros):
        try:
            return success_response(self.repository.custo_moto(dados_token, filtros), "Custo moto listada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def lucro_moto(self, dados_token, filtros):
        try:
            return success_response(self.repository.lucro_moto(dados_token, filtros), "Lucro moto listada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)