from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_, and_
from models.Franqueado import Franqueado
from models.FranquiaFraqueadoLocatario import FranquiaFraqueadoLocatario 
from config.funcoes import remove_campos, apenasNumeros
from config.filtros import filtros_basicos_franquiado
import os
import re


class FranquiadosRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_franquiados(self, data):

        cnpj = apenasNumeros(data["cnpj"])
        cpf = apenasNumeros(data["cpf"])
        status = data["status"]
        campos_para_remover = ["cpf", "cnpj","status"]
        dados_franquiado = remove_campos(data, campos_para_remover)
        dados_franquiado["cnpj"] = cnpj
        dados_franquiado["cpf"] = cpf
        dados_franquiado["status_id"] = status

        try:
            franquiado = Franqueado(**dados_franquiado)
            self.db.add(franquiado)
            self.db.commit()
            self.db.refresh(franquiado)
            return dados_franquiado
        
        except IntegrityError:
            self.db.rollback()
            raise ValueError("cnpj do franqueado já cadastrado")

        except Exception as e:
            self.db.rollback()
            raise e

    def update_franquiados(self, franquiado_id, data):
        try:
            franquiado = self.db.query(Franqueado).filter(
                Franqueado.id == franquiado_id
            ).first()
            
            if not franquiado:
                raise ValueError("Franqueado não encontrado")

            status = data.get("status")

            campos_para_remover = ["cnpj", "status"]
            dados_franquiado = remove_campos(data, campos_para_remover)
            dados_franquiado["status_id"] = status

            for campo, valor in dados_franquiado.items():
                if hasattr(franquiado, campo):
                    setattr(franquiado, campo, valor)
            
            self.db.commit()
            self.db.refresh(franquiado)
            return dados_franquiado.items()

        except IntegrityError:
            self.db.rollback()
            raise ValueError("CNPJ já cadastrado")

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_franquiados(self, franquiado_id):
        try:
            franquiado = self.db.query(Franqueado).filter(
                Franqueado.id == franquiado_id
            ).first()

            if not franquiado:
                raise ValueError("Franqueado não encontrada")

            self.db.delete(franquiado)
            self.db.commit()

            return {"message": "Franqueado removida com sucesso"}

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_franquiados(self, franquiado_id, ativa):
        try:
            franquiado = self.db.query(Franqueado).filter(
                Franqueado.id == franquiado_id
            ).first()

            if not franquiado:
                raise ValueError("Franqueado não encontrada")

            if ativa == 2:
                franquiado.deleted_at = func.now()

            elif ativa == 1:
                franquiado.deleted_at = None

            franquiado.status_id = ativa

            self.db.commit()
            self.db.refresh(franquiado)

            return {
                "id": franquiado.id,
                "status_id": franquiado.status_id,
                "deleted_at": franquiado.deleted_at
            }

        except Exception as e:
            self.db.rollback()
            raise e

    def listar_franquiados(self, dados_token, filtros):
        try:
            dados = dados_token["dados"]
            tipo_acesso = dados.get("tipoAcessoID")
            franquiado = dados.get("franquiado_id")

            query = (
                self.db.query(Franqueado, FranquiaFraqueadoLocatario)
                .outerjoin(
                    FranquiaFraqueadoLocatario,
                    and_(
                        FranquiaFraqueadoLocatario.franquiado_id == Franqueado.id,
                        FranquiaFraqueadoLocatario.locatarios_id == None,
                    )
                )
            )
            # adicionar o franquia_franquiador_locatario_id
            query = filtros_basicos_franquiado(query, filtros)
            if tipo_acesso != 1:
                query = query.filter(Franqueado.id == franquiado) 
            franquiados = query.all()
            saida = []
            for franquiado, franquiafraqueadolocatario in franquiados:

                item = {**franquiado.__dict__}
                item["franquia_franquiador_locatario_id"] = franquiafraqueadolocatario.id if franquiafraqueadolocatario else None 
                saida.append(item)

            return saida            

        except Exception as e:
            self.db.rollback()
            raise e