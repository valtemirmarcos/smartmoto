import os
from repositories.NotasRepository import NotasRepository
from config.funcoes import success_response, exception_response


class NotasController:
    def __init__(self, db):
        self.repository = NotasRepository(db)

    def create_notas(self, data):
        try:
            return success_response(self.repository.create_notas(data), "Nota cadastrada com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_notas(self, nota_id, data):
        try:
            return success_response(self.repository.update_notas(nota_id,data), "Nota alterada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_notas(self, nota_id):
        try:
            return success_response(self.repository.delete_notas(nota_id), "Nota deletada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_notas(self, nota_id, ativa):
        try:
            mensagem = "Nota desativada com sucesso"
            if ativa == 1:
                mensagem = "Nota ativada com sucesso"

            return success_response(self.repository.sfdelete_notas(nota_id, ativa), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)