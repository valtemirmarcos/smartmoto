from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_, and_

from models.Oficina import Oficina
from models.Frota import Frota
from models.FranquiaFraqueadoLocatario import FranquiaFraqueadoLocatario
from models.Locatario import Locatario
from models.User import User
from models.Franqueado import Franqueado

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios, formatar_placa

import os
import re
from config.filtros import filtro_basico_token, filtros_basicos_oficina

class OficinaRepository:
    def __init__(self, db: Session):
        self.db = db



    def create_oficina(self, data, dados_token):

        campos_obrigatorios = [
            "franquia_franquiador_locatario_id",
            "frota_id",
            "data_servico",
            "descricao",
            "valor"
        ]
        saida = validar_campos_obrigatorios(campos_obrigatorios, data)
        data['log_id'] = dados_token['dados']['id']
        dados_oficina = data
        try:

            oficina = Oficina(**dados_oficina)
            self.db.add(oficina)
            self.db.commit()
            self.db.refresh(oficina)
            return oficina
    
        except Exception as e:
            self.db.rollback()
            raise e

    def update_oficina(self, oficina_id, data, dados_token):
        try:
            data['log_id'] = dados_token['dados']['id']
            oficina = self.db.query(Oficina).filter(
                Oficina.id == oficina_id
            ).first()
            if not oficina:
                raise ValueError("servico não encontrado")

            campos_para_remover = ["franquia_franquiador_locatario_id", "frota_id"]
            dados_oficina = remove_campos(data, campos_para_remover)

            for campo, valor in dados_oficina.items():
                setattr(oficina, campo, valor)
                
            self.db.commit()
            self.db.refresh(oficina)

            return oficina

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_oficina(self, oficina_id):
        try:
            oficina = self.db.query(Oficina).filter(
                Oficina.id == oficina_id
            ).first()
            if not oficina:
                raise ValueError("servico não encontrado")

            self.db.delete(oficina)
            self.db.commit()

            return {"message": "Nota removida com sucesso"}

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_oficina(self, oficina_id, ativa, dados_token):
        try:
            log_id = dados_token['dados']['id']
            oficina = self.db.query(Oficina).filter(
                Oficina.id == oficina_id
            ).first()
            if not oficina:
                raise ValueError("servico não encontrado")

            if ativa == 2:
                oficina.deleted_at = func.now()

            elif ativa == 1:
                oficina.deleted_at = None

            oficina.status_id = ativa
            oficina.log_id = log_id

            self.db.commit()
            self.db.refresh(oficina)

            return oficina

        except Exception as e:
            self.db.rollback()
            raise e

    def listar_oficina(self, dados_token, filtro):
        try:
            dados = dados_token['dados']
            parametros = ["franquia_id","franquiado_id","locatarios_id"]

            filtro_token = filtro_basico_token(FranquiaFraqueadoLocatario, dados, parametros)
            query = (
                self.db.query(Oficina, Frota, Locatario, User, Franqueado)
                .join(
                    Frota,
                    Frota.id == Oficina.frota_id
                )
                .join(
                    Franqueado,
                    Franqueado.id == Frota.fraqueado_id,
                )
                .join(
                    Locatario,
                    Locatario.frota_id == Oficina.frota_id
                )
                .outerjoin(
                    FranquiaFraqueadoLocatario,
                    and_(
                        FranquiaFraqueadoLocatario.franquiado_id == Frota.fraqueado_id,
                        FranquiaFraqueadoLocatario.locatarios_id == Locatario.id,
                    )
                )
                .outerjoin(
                    User,
                    User.id == Oficina.log_id
                )
                .filter(
                    Oficina.deleted_at.is_(None)
                )
                .filter(
                    Locatario.status_id == 1
                )
            )

            query = filtros_basicos_oficina(query, filtro)
            oficinas = query.filter(*filtro_token).all()
            saida = []
            for oficina, frota, locatario, user, franqueado in oficinas:
                item = {**oficina.__dict__}
                item['placa'] = formatar_placa(frota.placa) if frota else None
                item['placasf'] = frota.placa if frota else None
                item["usuario"] = user.nome if user else None
                item["locatario"] = locatario.nome if locatario else None
                item["fraqueado"] = franqueado.nome if franqueado else None
                saida.append(item)

            # sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
            # return {"sql": filtro}
            return saida
            oficina = query.all()
            return oficina

        except Exception as e:
            self.db.rollback()
            raise e