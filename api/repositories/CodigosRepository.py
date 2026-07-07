from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from models.Codigo import Codigo

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios

import os
import re


class CodigosRepository:
    def __init__(self, db: Session):
        self.db = db


    def create_codigos(self, data, dados_token):
        campos_obrigatorios = [
            "codigo",
            "depara_id",
            "descricao",
            "obs"
        ]
        saida = validar_campos_obrigatorios(campos_obrigatorios, data)
        data['log_id'] = dados_token['dados']['id']
        dados_codigos = data
        try:

            codigo = Codigo(**dados_codigos)
            self.db.add(codigo)
            self.db.commit()
            self.db.refresh(codigo)
            return codigo
    
        except Exception as e:
            self.db.rollback()
            raise e

    def update_codigos(self, codigo_id, data, dados_token):
        try:
            data['log_id'] = dados_token['dados']['id']
            
            codigo = self.db.query(Codigo).filter(
                Codigo.id == codigo_id
            ).first()
            if not codigo:
                raise ValueError("codigo não encontrado")
            
            campos_para_remover = ["franquia_franquiador_locatario_id", "frota_id"]
            dados_calcao = remove_campos(data, campos_para_remover)

            for campo, valor in dados_calcao.items():
                setattr(codigo, campo, valor)
                
            self.db.commit()
            self.db.refresh(codigo)

            return codigo

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_codigos(self, codigo_id, dados_token):
        try:
            codigo = self.db.query(Codigo).filter(
                Codigo.id == codigo_id
            ).first()
            if not codigo:
                raise ValueError("codigo não encontrado")

            self.db.delete(codigo)
            self.db.commit()

            return {"message": "Codigo removido com sucesso"}

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_codigos(self, codigo_id, ativa, dados_token):
        try:
            codigo = self.db.query(Codigo).filter(
                Codigo.id == codigo_id
            ).first()
            if not codigo:
                raise ValueError("codigo não encontrado")

            if ativa == 2:
                codigo.deleted_at = func.now()

            elif ativa == 1:
                codigo.deleted_at = None


            self.db.commit()
            self.db.refresh(codigo)

            return codigo

        except Exception as e:
            self.db.rollback()
            raise e