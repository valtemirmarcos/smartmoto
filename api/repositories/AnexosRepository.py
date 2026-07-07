from sqlalchemy.orm import Session, aliased
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_, and_, extract

from models.Semanal import Semanal
from models.Frota import Frota
from models.Locatario import Locatario
from models.Plano import Plano
from models.FranquiaFraqueadoLocatario import FranquiaFraqueadoLocatario
from models.Codigo import Codigo
from models.User import User
from models.Franqueado import Franqueado
from models.Franquia import Franquia
from models.Anexo import Anexo

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios, dia_semana_extenso, datas_do_dia_semana_mes, filtro_basico, formatar_placa
from config.filtros import filtros_basicos_anexos
import os
import re

from datetime import date, timedelta
import calendar
import base64
from fastapi.responses import Response
from config.supabase_storage_service import SupabaseStorageService

class AnexosRepository:
    def __init__(self, db: Session):
        self.db = db


    def create_anexos(self, data, dados_token):
        
        campos_obrigatorios = [
            "entidade_tipo",
            "entidade_id"
        ]
        saida = validar_campos_obrigatorios(campos_obrigatorios, data)
        franquia_franquiador_locatario_id = data.get('franquia_franquiador_locatario_id')
        storage_service = SupabaseStorageService()

        arquivo_drive = storage_service.upload_file(
            data['file'],
            data['entidade_tipo'],
            data['entidade_id'],
            franquia_franquiador_locatario_id  # None se não vier
        )

        dados_anexos = {
            "franquia_franquiador_locatario_id": franquia_franquiador_locatario_id,
            "entidade_tipo":data['entidade_tipo'],
            "entidade_id": data['entidade_id'],
            "log_id": dados_token['dados']['id'],
            "nome_arquivo": data['file'].filename,
            "tipo_mime": data['file'].content_type,
            "drive_file_id": arquivo_drive["id"],
            "drive_link": arquivo_drive.get("webViewLink")
        }

        try:

            anexo = Anexo(**dados_anexos)
            self.db.add(anexo)
            self.db.commit()
            self.db.refresh(anexo)
            return anexo
        

        except Exception as e:
            self.db.rollback()
            raise e

    def update_anexos(self, anexo_id, data, dados_token):
        try:
            anexo = self.db.query(Anexo).filter(
                Anexo.id == anexo_id
            ).first()
            if not anexo:
                raise ValueError("arquivo não encontrado")

            storage_service = SupabaseStorageService()

            # Remove o arquivo antigo do Storage antes de fazer upload do novo
            if anexo.drive_file_id:
                storage_service.delete_file(anexo.drive_file_id)

            # Faz upload do novo arquivo
            arquivo_drive = storage_service.upload_file(
                data['file'],
                anexo.franquia_franquiador_locatario_id,
                anexo.entidade_tipo,
                anexo.entidade_id
            )

            dados_anexos = {
                "log_id": dados_token['dados']['id'],
                "nome_arquivo": data['file'].filename,
                "tipo_mime": data['file'].content_type,
                "drive_file_id": arquivo_drive["id"],
                "drive_link": arquivo_drive.get("webViewLink")
            }

            for campo, valor in dados_anexos.items():
                setattr(anexo, campo, valor)

            self.db.commit()
            self.db.refresh(anexo)
            return anexo

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_anexos(self, anexo_id, dados_token):
        try:
            anexo = self.db.query(Anexo).filter(
                Anexo.id == anexo_id
            ).first()
            url = anexo.drive_file_id
            if not anexo:
                raise ValueError("arquivo não encontrado")

            self.db.delete(anexo)
            self.db.commit()

            storage_service = SupabaseStorageService()
            if anexo.drive_file_id:
                storage_service.delete_file(anexo.drive_file_id)


            return {"message": "arquivo removido com sucesso"}

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_anexos(self, anexo_id, ativa, dados_token):
        try:

            log_id = dados_token['dados']['id']
            anexo = self.db.query(Anexo).filter(
                Anexo.id == anexo_id
            ).first()
            if not anexo:
                raise ValueError("arquivo não encontrado")

            if ativa == 0:
                anexo.deleted_at = func.now()

            elif ativa == 1:
                anexo.deleted_at = None

            anexo.log_id = log_id

            self.db.commit()
            self.db.refresh(anexo)

            return anexo

        except Exception as e:
            self.db.rollback()
            raise e


    def listar_anexos(self, dados_token, filtro):
        try:
            dados = dados_token['dados']
            parametros = ["franquia_id","franquiado_id","locatarios_id"]

            # filtro_token = filtro_basico(FranquiaFraqueadoLocatario, dados, parametros)
            query = (
                self.db.query(Anexo)
                .outerjoin(
                    FranquiaFraqueadoLocatario,
                    FranquiaFraqueadoLocatario.id == Anexo.franquia_franquiador_locatario_id,
                )
                .outerjoin(
                    Franquia,
                    Franquia.id == FranquiaFraqueadoLocatario.franquia_id
                )
                .outerjoin(
                    Franqueado,
                    Franqueado.id == FranquiaFraqueadoLocatario.franquiado_id
                )
                .outerjoin(
                    Locatario,
                    Locatario.id == FranquiaFraqueadoLocatario.locatarios_id
                )
            )
            query = filtros_basicos_anexos(query, filtro)

            anexos = query.all()
            return anexos

        except Exception as e:
            self.db.rollback()
            raise e

    def ler_imagem(self, tipo, codigo):
        return self.db.query(Anexo).filter(
            Anexo.entidade_tipo == tipo,
            Anexo.entidade_id == codigo
        ).first()

