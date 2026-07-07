from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from models.Nota import Nota

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios

import os
import re


class NotasRepository:
    def __init__(self, db: Session):
        self.db = db



    def create_notas(self, data):

        campos_obrigatorios = [
            "franquiador_id",
            "frota_id",
            "valor_bruto_rateado",
            "valor_liquido_rateado"
        ]
        saida = validar_campos_obrigatorios(campos_obrigatorios, data)

        dados_notas = data
        try:

            nota = Nota(**dados_notas)
            self.db.add(nota)
            self.db.commit()
            self.db.refresh(nota)
            return nota
    
        except Exception as e:
            self.db.rollback()
            raise e

    def update_notas(self, nota_id, data):
        try:

            nota = self.db.query(Nota).filter(
                Nota.id == nota_id
            ).first()
            if not nota:
                raise ValueError("nota não encontrada")

            campos_para_remover = ["franquiador_id", "frota_id"]
            dados_nota = remove_campos(data, campos_para_remover)

            self.db.commit()
            self.db.refresh(nota)

            return nota

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_notas(self, nota_id):
        try:
            nota = self.db.query(Nota).filter(
                Nota.id == nota_id
            ).first()
            if not nota:
                raise ValueError("Nota não encontrada")

            self.db.delete(nota)
            self.db.commit()

            return {"message": "Nota removida com sucesso"}

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_notas(self, nota_id, ativa):
        try:
            nota = self.db.query(Nota).filter(
                Nota.id == nota_id
            ).first()
            if not nota:
                raise ValueError("Nota não encontrada")

            if ativa == 2:
                nota.deleted_at = func.now()

            elif ativa == 1:
                nota.deleted_at = None

            nota.status_id = ativa

            self.db.commit()
            self.db.refresh(nota)

            return nota

        except Exception as e:
            self.db.rollback()
            raise e