import os
from repositories.BasicRepository import BasicRepository
from config.funcoes import success_response, exception_response
basicRepository = BasicRepository()

class BasicController:
    def helloa(self):
        try:
            return success_response(data=basicRepository.helloa())
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception:
            return exception_response("Erro interno", 500)
    def hello(self):
        return basicRepository.hello()

    def db_info(self):
        return basicRepository.db_info()