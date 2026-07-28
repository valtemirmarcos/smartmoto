from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from models.Codigo import Codigo
from models.Plano import Plano

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios

import os
import re


class FiltrosRepository:
    def __init__(self, db: Session):
        self.db = db

    def frota_status(self):

        try:
            saida = (
                    self.db.query(
                    Codigo.codigo.label("id"),
                    Codigo.descricao.label("texto")
                ).filter(Codigo.depara_id == 2).all()
            )
            return [dict(row._mapping) for row in saida]
    
        except Exception as e:
            self.db.rollback()
            raise e

    def locatario_status(self):

        try:
            saida = (
                    self.db.query(
                    Codigo.codigo.label("id"),
                    Codigo.descricao.label("texto")
                ).filter(Codigo.depara_id == 1)
                .order_by(Codigo.codigo).all()
            )
            return [dict(row._mapping) for row in saida]
    
        except Exception as e:
            self.db.rollback()
            raise e

    def calcao_status(self):

        try:
            saida = (
                    self.db.query(
                    Codigo.codigo.label("id"),
                    Codigo.descricao.label("texto")
                ).filter(Codigo.depara_id == 4)
                .order_by(Codigo.codigo).all()
            )
            return [dict(row._mapping) for row in saida]
    
        except Exception as e:
            self.db.rollback()
            raise e

    def filtro_planos(self):

        try:
            saida = (
                    self.db.query(
                    Plano.id.label("id"),
                    Plano.plano.label("texto")
                    )
                    .order_by(Plano.id).all()
            )
            return [dict(row._mapping) for row in saida]
    
        except Exception as e:
            self.db.rollback()
            raise e
            
    def semanais_status(self):

        try:
            saida = (
                    self.db.query(
                    Codigo.codigo.label("id"),
                    Codigo.descricao.label("texto")
                ).filter(Codigo.depara_id == 3)
                .order_by(Codigo.codigo).all()
            )
            return [dict(row._mapping) for row in saida]
    
        except Exception as e:
            self.db.rollback()
            raise e

    def multas_status(self):

        try:
            saida = (
                    self.db.query(
                    Codigo.codigo.label("id"),
                    Codigo.descricao.label("texto")
                ).filter(Codigo.depara_id == 6)
                .order_by(Codigo.codigo).all()
            )
            return [dict(row._mapping) for row in saida]
    
        except Exception as e:
            self.db.rollback()
            raise e

    def faturamentos_status(self):

        try:
            saida = (
                    self.db.query(
                    Codigo.codigo.label("id"),
                    Codigo.descricao.label("texto")
                ).filter(Codigo.depara_id == 8)
                .order_by(Codigo.codigo).all()
            )
            return [dict(row._mapping) for row in saida]
    
        except Exception as e:
            self.db.rollback()
            raise e

    def faturamentos_tipos(self):

        try:
            saida = (
                    self.db.query(
                    Codigo.codigo.label("id"),
                    Codigo.descricao.label("texto")
                ).filter(Codigo.depara_id == 7)
                .order_by(Codigo.codigo).all()
            )
            return [dict(row._mapping) for row in saida]
    
        except Exception as e:
            self.db.rollback()
            raise e

    def filtro_pagamentos(self):
        try:
            saida = (
                    self.db.query(
                    Codigo.codigo.label("id"),
                    Codigo.descricao.label("texto")
                ).filter(Codigo.depara_id == 5)
                .order_by(Codigo.codigo).all()
            )
            return [dict(row._mapping) for row in saida]
    
        except Exception as e:
            self.db.rollback()
            raise e

    def custos_status(self):
        try:
            saida = (
                    self.db.query(
                    Codigo.codigo.label("id"),
                    Codigo.descricao.label("texto")
                ).filter(Codigo.depara_id == 9)
                .order_by(Codigo.codigo).all()
            )
            return [dict(row._mapping) for row in saida]
    
        except Exception as e:
            self.db.rollback()
            raise e
