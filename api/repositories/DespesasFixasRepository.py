from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from models.DespesaFixa import DespesaFixa

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios

import os
import re


class DespesasFixasRepository:
    def __init__(self, db: Session):
        self.db = db



    def create_despesas_fixas(self, data):

        campos_obrigatorios = [
            "franquia_franquiador_locatario_id",
            "frota_id",
            "descricao",
            "valor"
        ]
        saida = validar_campos_obrigatorios(campos_obrigatorios, data)

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

    def update_despesas_fixas(self, despesa_fixa_id, data):
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

    def delete_despesas_fixas(self, despesa_fixa_id):
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

    def sfdelete_despesas_fixas(self, despesa_fixa_id, ativa):
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