import os
from repositories.FranquiadosRepository import FranquiadosRepository
from config.funcoes import success_response, exception_response


class FranquiadosController:
    def __init__(self, db):
        self.repository = FranquiadosRepository(db)

    def create_franquiados(self, data, dados_token):
        try:
            return success_response(self.repository.create_franquiados(data, dados_token), "Franqueado cadastrado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_franquiados(self, franquiado_id, data, dados_token):
        try:
            return success_response(self.repository.update_franquiados(franquiado_id,data, dados_token), "Franquiado alterado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_franquiados(self, franquiado_id, dados_token):
        try:
            return success_response(self.repository.delete_franquiados(franquiado_id, dados_token), "Franquiado deletado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_franquiados(self, franquiado_id, ativa, dados_token):
        try:
            mensagem = "Franquiado desativado com sucesso"
            if ativa == 1:
                mensagem = "Franquiado ativado com sucesso"

            return success_response(self.repository.sfdelete_franquiados(franquiado_id, ativa, dados_token), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)


    def listar_franquiados(self, dados_token, filtros):
        try:
            return success_response(self.repository.listar_franquiados(dados_token, filtros), "Franquiado listado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)