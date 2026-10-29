from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, case

from models.Plano import Plano

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios
from config.filtros import filtros_basicos_planos
import os
import re


class PlanosRepository:
    def __init__(self, db: Session):
        self.db = db



    def create_planos(self, data, dados_token):
        data['log_id'] = dados_token['dados']['id']
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

    def update_planos(self, plano_id, data, dados_token):
        try:
            data['log_id'] = dados_token['dados']['id']
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

    def delete_planos(self, plano_id, dados_token):
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

    def sfdelete_planos(self, plano_id, ativa, dados_token):
        try:
            log_id = dados_token['dados']['id']
            plano = self.db.query(Plano).filter(
                Plano.id == plano_id
            ).first()
            if not plano:
                raise ValueError("plano não encontrado")

            if ativa == 2:
                plano.deleted_at = func.now()

            elif ativa == 1:
                plano.deleted_at = None

            plano.log_id = log_id

            self.db.commit()
            self.db.refresh(plano)

            return plano

        except Exception as e:
            self.db.rollback()
            raise e

    def listar_planos(self, dados_token, filtro):
        try:
            dados = dados_token['dados']

            query = self.db.query(Plano)

            query = filtros_basicos_planos(query, filtro)

            query = query.order_by(
                case(
                    (Plano.deleted_at.is_(None), 1),
                    else_=2
                ).asc()
            )

            listarPlanos = query.all()

            for plano in listarPlanos:
                plano.status = 1 if plano.deleted_at is None else 2

            return listarPlanos

        except Exception as e:
            self.db.rollback()
            raise e