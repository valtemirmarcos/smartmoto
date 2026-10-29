from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_, and_

from models.DespesaFixa import DespesaFixa
from models.Franqueado import Franqueado
from models.FranquiaFraqueadoLocatario import FranquiaFraqueadoLocatario
from models.User import User
from models.Frota import Frota

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios
from config.filtros import filtro_basico_token, filtros_basicos_despesas_fixas

import os
import re


class DespesasFixasRepository:
    def __init__(self, db: Session):
        self.db = db



    def create_despesas_fixas(self, data, dados_token):
        campos_obrigatorios = [
            "franquia_franquiador_locatario_id",
            "frota_id",
            "descricao",
            "valor"
        ]

        saida = validar_campos_obrigatorios(campos_obrigatorios, data)
        data['log_id'] = dados_token['dados']['id']
        dados_despesas_fixas = data
        try:
            despesa_fixa = DespesaFixa(**dados_despesas_fixas)
            self.db.add(despesa_fixa)
            self.db.commit()
            self.db.refresh(despesa_fixa)
            return despesa_fixa
        

        except Exception as e:
            self.db.rollback()
            raise e

    def update_despesas_fixas(self, despesa_fixa_id, data, dados_token):
        try:

            despesa_fixa = self.db.query(DespesaFixa).filter(
                DespesaFixa.id == despesa_fixa_id
            ).first()
            if not despesa_fixa:
                raise ValueError("despesa_fixa não encontrada")

            campos_para_remover = ["franquia_franquiador_locatario_id", "frota_id"]
            dados_despesa_fixa = remove_campos(data, campos_para_remover)

            for campo, valor in dados_despesa_fixa.items():
                setattr(despesa_fixa, campo, valor)
                
            self.db.commit()
            self.db.refresh(despesa_fixa)

            return despesa_fixa

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_despesas_fixas(self, despesa_fixa_id, dados_token):
        try:
            despesa_fixa = self.db.query(DespesaFixa).filter(
                DespesaFixa.id == despesa_fixa_id
            ).first()
            if not despesa_fixa:
                raise ValueError("despesa_fixa não encontrada")

            self.db.delete(despesa_fixa)
            self.db.commit()

            return {"message": "DespesaFixa removida com sucesso"}

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_despesas_fixas(self, despesa_fixa_id, ativa, dados_token):
        try:
            despesa_fixa = self.db.query(DespesaFixa).filter(
                DespesaFixa.id == despesa_fixa_id
            ).first()
            if not despesa_fixa:
                raise ValueError("despesa_fixa não encontrada")

            if ativa == 2:
                despesa_fixa.deleted_at = func.now()

            elif ativa == 1:
                despesa_fixa.deleted_at = None

            despesa_fixa.status_id = ativa

            self.db.commit()
            self.db.refresh(despesa_fixa)

            return despesa_fixa

        except Exception as e:
            self.db.rollback()
            raise e

    def listar_despesas_fixas(self, dados_token, filtro):
        try:
            

            franquiado_id = dados_token['dados']['franquiado_id']
            franquia_id = dados_token['dados']['franquia_id']
            locatario_id = dados_token['dados']['locatarios_id']

            # if locatario_id is not None:
            #     return None

            query = (
                self.db.query(DespesaFixa, User, Franqueado, Frota)
                .select_from(DespesaFixa)
                .join(
                    Frota,
                    Frota.id == DespesaFixa.frota_id
                )
                .join(
                    Franqueado,
                    Franqueado.id == franquiado_id
                )
                .join(
                    FranquiaFraqueadoLocatario,
                    and_(
                        FranquiaFraqueadoLocatario.franquiado_id == franquiado_id,
                        FranquiaFraqueadoLocatario.franquia_id == franquia_id,
                    )
                )
                .outerjoin(
                    User,
                    User.id == DespesaFixa.log_id
                )
                .filter(
                    DespesaFixa.deleted_at.is_(None)
                )
            )
            query = filtros_basicos_despesas_fixas(query, filtro)
            despesas = query.all()

            saida = []
            for despesa, user, franqueado, frota in despesas:
                item = {**despesa.__dict__}
                item["usuario"] = user.nome if user else None
                item["franqueado"] = franqueado.nome if franqueado else None
                item["franqueado_id"] = franqueado.id if franqueado else None
                item["placa"] = frota.placa if frota else None
                saida.append(item)

            # # sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
            # # return {"sql": filtro}
            return saida

        except Exception as e:
            self.db.rollback()
            raise e