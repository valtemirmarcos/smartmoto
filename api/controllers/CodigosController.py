import os
from repositories.CodigosRepository import CodigosRepository
from config.funcoes import success_response, exception_response


class CodigosController:
    def __init__(self, db):
        self.repository = CodigosRepository(db)

    def create_codigos(self, data, dados_token):
        try:
            return success_response(self.repository.create_codigos(data, dados_token), "Parametro cadastrado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_codigos(self, codigo_id, data, dados_token):
        try:
            return success_response(self.repository.update_codigos(codigo_id, data, dados_token), "Parametro alterado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_codigos(self, codigo_id, dados_token):
        try:
            return success_response(self.repository.delete_codigos(codigo_id, dados_token), "Parametro deletado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_codigos(self, codigo_id, ativa, dados_token):
        try:
            mensagem = "Parametro desativado com sucesso"
            if ativa == 1:
                mensagem = "Parametro ativado com sucesso"

            return success_response(self.repository.sfdelete_codigos(codigo_id, ativa, dados_token), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)