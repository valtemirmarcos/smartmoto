from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from models.Plano import Plano

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios

import os
import re


class PlanosRepository:
    def __init__(self, db: Session):
        self.db = db



    def create_planos(self, data):

        campos_obrigatorios = [
            "plano",
            "descricao",
            "semanas"
        ]
        saida = validar_campos_obrigatorios(campos_obrigatorios, data)

        dados_planos = data
        try:

            plano = Plano(**dados_planos)
            self.db.add(plano)
            self.db.commit()
            self.db.refresh(plano)
            return plano
    
        except Exception as e:
            self.db.rollback()
            raise e

    def update_planos(self, plano_id, data):
        try:
            
            plano = self.db.query(Plano).filter(
                Plano.id == plano_id
            ).first()
            if not plano:
                raise ValueError("plano não encontrado")

            for campo, valor in data.items():
                setattr(plano, campo, valor)

            self.db.commit()
            self.db.refresh(plano)

            return plano

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_planos(self, plano_id):
        try:
            plano = self.db.query(Plano).filter(
                Plano.id == plano_id
            ).first()
            if not plano:
                raise ValueError("plano não encontrado")

            self.db.delete(plano)
            self.db.commit()

            return {"message": "Plano removido com sucesso"}

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_planos(self, plano_id, ativa):
        try:
            plano = self.db.query(Plano).filter(
                Plano.id == plano_id
            ).first()
            if not plano:
                raise ValueError("plano não encontrado")

            if ativa == 2:
                plano.deleted_at = func.now()

            elif ativa == 1:
                plano.deleted_at = None


            self.db.commit()
            self.db.refresh(plano)

            return plano

        except Exception as e:
            self.db.rollback()
            raise e