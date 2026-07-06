import os
from repositories.UsersRepository import UsersRepository
from config.funcoes import success_response, exception_response, ler_token


class UsersController:
    def __init__(self, db):
        self.repository = UsersRepository(db)

    def helloa(self):
        try:
            return success_response(data=self.repository.helloa())
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception:
            return exception_response("Erro interno", 500)
    def hello(self):
        return self.repository.hello()

    def db_info(self):
        return self.repository.db_info()

    def create_user(self, data, request, dados_token):
        try:
            return success_response(self.repository.create_user(data, dados_token))
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_user(self, data, user_id, request, dados_token):
        try:

            return success_response(self.repository.update_users(user_id, data, dados_token, request), "Usuario alterado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_users(self, user_id, ativa, request, dados_token):
        try:

            mensagem = "Usuário desativado com sucesso"
            if ativa == 1:
                mensagem = "Usuário ativado com sucesso"

            return success_response(self.repository.sfdelete_users(user_id, ativa, dados_token), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def login(self, data):
        try:
            return success_response(self.repository.login(data))
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)