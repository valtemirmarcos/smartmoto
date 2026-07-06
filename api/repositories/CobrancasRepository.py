from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from models.Despesa import Despesa as Cobranca

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios

import os
import re


class CobrancasRepository:
    def __init__(self, db: Session):
        self.db = db



    def create_cobrancas(self, data):

        campos_obrigatorios = [
            "franquia_franquiador_locatario_id",
            "frota_id",
            "data",
            "descricao",
            "valor"
        ]
        saida = validar_campos_obrigatorios(campos_obrigatorios, data)

        dados_cobrancas = data
        try:

            cobranca = Cobranca(**dados_cobrancas)
            self.db.add(cobranca)
            self.db.commit()
            self.db.refresh(cobranca)
            return cobranca
        

        except Exception as e:
            self.db.rollback()
            raise e

    def update_cobrancas(self, cobranca_id, data):
        try:

            cobranca = self.db.query(Cobranca).filter(
                Cobranca.id == cobranca_id
            ).first()
            if not cobranca:
                raise ValueError("cobranca não encontrada")

            campos_para_remover = ["franquia_franquiador_locatario_id", "frota_id", "codigo"]
            dados_multa = remove_campos(data, campos_para_remover)

            self.db.commit()
            self.db.refresh(cobranca)

            return cobranca

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_cobrancas(self, cobranca_id):
        try:
            cobranca = self.db.query(Cobranca).filter(
                Cobranca.id == cobranca_id
            ).first()
            if not cobranca:
                raise ValueError("cobranca não encontrada")

            self.db.delete(cobranca)
            self.db.commit()

            return {"message": "Cobranca removida com sucesso"}

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_cobrancas(self, cobranca_id, ativa):
        try:
            cobranca = self.db.query(Cobranca).filter(
                Cobranca.id == cobranca_id
            ).first()
            if not cobranca:
                raise ValueError("cobranca não encontrada")

            if ativa == 2:
                cobranca.deleted_at = func.now()

            elif ativa == 1:
                cobranca.deleted_at = None

            cobranca.status_id = ativa

            self.db.commit()
            self.db.refresh(cobranca)

            return cobranca

        except Exception as e:
            self.db.rollback()
            raise e