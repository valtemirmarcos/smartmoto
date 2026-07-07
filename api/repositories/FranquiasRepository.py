from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from models.Franquia import Franquia
import os
import re


class FranquiasRepository:
    def __init__(self, db: Session):
        self.db = db



    def create_franquias(self, data):
        cnpj = data["cnpj"]
        cnplimpo = re.sub(r"\D", "", cnpj)
        dados_franquia = {
            "franquia": data["rasaosocial"],
            "cnpj": cnplimpo,
            "status_id": data["status"]
        }
        try:
            franquia = Franquia(**dados_franquia)
            self.db.add(franquia)
            self.db.commit()
            self.db.refresh(franquia)
            saida_franquia = {
                "franquia": franquia.franquia,
                "cnpj": franquia.cnpj,
                "status_id": franquia.status_id
            }
            return saida_franquia
        
        except IntegrityError:
            self.db.rollback()
            raise ValueError("cnpj já cadastrado")

        except Exception as e:
            self.db.rollback()
            raise e

    def update_franquias(self, franquia_id, data):
        try:
            franquia = self.db.query(Franquia).filter(
                Franquia.id == franquia_id
            ).first()

            if not franquia:
                raise ValueError("Franquia não encontrada")

            if "rasaosocial" in data:
                franquia.franquia = data["rasaosocial"]

            if "cnpj" in data:
                cnplimpo = re.sub(r"\D", "", data["cnpj"])
                franquia.cnpj = cnplimpo

            if "status" in data:
                franquia.status_id = data["status"]

            self.db.commit()
            self.db.refresh(franquia)

            return {
                "id": franquia.id,
                "franquia": franquia.franquia,
                "cnpj": franquia.cnpj,
                "status_id": franquia.status_id
            }

        except IntegrityError:
            self.db.rollback()
            raise ValueError("CNPJ já cadastrado")

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_franquias(self, franquia_id):
        try:
            franquia = self.db.query(Franquia).filter(
                Franquia.id == franquia_id
            ).first()

            if not franquia:
                raise ValueError("Franquia não encontrada")

            self.db.delete(franquia)
            self.db.commit()

            return {"message": "Franquia removida com sucesso"}

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_franquias(self, franquia_id, ativa):
        try:
            franquia = self.db.query(Franquia).filter(
                Franquia.id == franquia_id
            ).first()

            if not franquia:
                raise ValueError("Franquia não encontrada")

            if ativa == 2:
                franquia.deleted_at = func.now()

            elif ativa == 1:
                franquia.deleted_at = None

            franquia.status_id = ativa

            self.db.commit()
            self.db.refresh(franquia)

            return {
                "id": franquia.id,
                "status_id": franquia.status_id,
                "deleted_at": franquia.deleted_at
            }

        except Exception as e:
            self.db.rollback()
            raise e