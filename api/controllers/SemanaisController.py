import os
from repositories.SemanaisRepository import SemanaisRepository
from config.funcoes import success_response, exception_response
from fastapi.responses import Response
import base64


class SemanaisController:
    def __init__(self, db):
        self.repository = SemanaisRepository(db)

    def create_semanais(self, data, dados_token):
        try:
            return success_response(self.repository.create_semanais(data, dados_token), "Semana cadastrada com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def update_semanais(self, semana_id, data, dados_token):
        try:
            return success_response(self.repository.update_semanais(semana_id, data, dados_token), "Semana alterada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def delete_semanais(self, semana_id, dados_token):
        try:
            return success_response(self.repository.delete_semanais(semana_id, dados_token), "Semana deletada com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def sfdelete_semanais(self, semana_id, ativa, dados_token):
        try:
            mensagem = "Semana desativada com sucesso"
            if ativa == 1:
                mensagem = "Semana ativada com sucesso"

            return success_response(self.repository.sfdelete_semanais(semana_id, ativa, dados_token), mensagem)
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def gerar_semanais(self, data, dados_token):
        try:
            return success_response(self.repository.gerar_semanais(data, dados_token), "Semanais cadastrados com sucesso!")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def listar_semanais(self, dados_token, filtro):
        try:
            return success_response(self.repository.listar_semanais(dados_token, filtro), "Semanais listados com sucesso")
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)

    def upload_imagem_semanal(self, semana_id, file, dados_token):
        try:
            conteudo = file.file.read()
            base64_str = base64.b64encode(conteudo).decode('utf-8')

            tipo_arquivo = file.content_type  # ex: image/png, application/pdf
            return success_response(
                self.repository.salvar_imagem_semanal(semana_id, base64_str, tipo_arquivo, dados_token),
                "Arquivo salvo com sucesso"
            )
        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)


    def get_imagem_semanal(self, semanal_id):
        try:
            semanal = self.repository.buscar_por_id(semanal_id)

            if not semanal or not semanal.imagem_base64:
                raise ValueError("Imagem não encontrada")

            arquivo_bytes = base64.b64decode(semanal.imagem_base64)

            return Response(
                content=arquivo_bytes,
                media_type=semanal.imagem_tipo,
                headers={
                    "Content-Disposition": "inline"
                }
            )

        except ValueError as e:
            return exception_response(str(e), 404)
        except Exception as error:
            return exception_response(str(error), 500)
