import os
from repositories.AnexosRepository import AnexosRepository
from config.funcoes import success_response, exception_response
from fastapi.responses import Response
import base64
from config.supabase_storage_service import SupabaseStorageService


class AnexosController:
    def __init__(self, db):
        self.repository = AnexosRepository(db)

    def create_anexos(self, data, dados_token):
        try:
            return success_response(self.repository.create_anexos(data, dados_token), "Arquivo cadastrado com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_anexos(self, anexo_id, data, dados_token):
        try:
            return success_response(self.repository.update_anexos(anexo_id, data, dados_token), "Arquivo alterado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_anexos(self, anexo_id, dados_token):
        try:
            return success_response(self.repository.delete_anexos(anexo_id, dados_token), "Arquivo deletado com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_anexos(self, anexo_id, ativa, dados_token):
        try:
            mensagem = "Arquivo desativado com sucesso"
            if ativa == 1:
                mensagem = "Arquivo ativado com sucesso"

            return success_response(self.repository.sfdelete_anexos(anexo_id, ativa, dados_token), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def listar_anexos(self, dados_token, filtro):
        try:
            return success_response(self.repository.listar_anexos(dados_token, filtro), "Arquivos listados com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)


    def ler_imagem(self, tipo, codigo):
        try:
            anexo = self.repository.ler_imagem(tipo, codigo)

            if not anexo or not anexo.drive_file_id:
                raise ValueError("Arquivo não encontrado")

            storage_service = SupabaseStorageService()
            arquivo_bytes = storage_service.download_file(anexo.drive_file_id)

            return Response(
                content=arquivo_bytes,
                media_type=anexo.tipo_mime,
                headers={
                    "Content-Disposition": "inline"
                }
            )

        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)
