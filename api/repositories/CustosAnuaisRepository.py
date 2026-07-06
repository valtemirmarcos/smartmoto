from sqlalchemy.orm import Session, aliased
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_, and_

from models.Frota import Frota
from models.CustosAnuais import CustosAnuais
from models.Locatario import Locatario
from models.FranquiaFraqueadoLocatario import FranquiaFraqueadoLocatario
from models.Codigo import Codigo
from models.User import User

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios, filtro_basico, formatar_placa
from config.filtros import filtros_basicos_custos_anuais

import os
import re


class CustosAnuaisRepository:
    def __init__(self, db: Session):
        self.db = db



    def create_custos_anuais(self, data, dados_token):
        campos_obrigatorios = [
            "frota_id",
            "data_vencimento",
            "parcela",
            "valor",
            "status_id",
            "custo"
        ]
        saida = validar_campos_obrigatorios(campos_obrigatorios, data)
        data['log_id'] = dados_token['dados']['id']
        dados_custos_anuais = data
        try:
            frota_id = dados_custos_anuais['frota_id']
            frota = self.db.query(Frota).filter(
                Frota.id == frota_id
            ).first()
            custos_anuais = CustosAnuais(**dados_custos_anuais)
            self.db.add(custos_anuais)
            self.db.commit()
            self.db.refresh(custos_anuais)
            return custos_anuais
        
        except IntegrityError:
            self.db.rollback()
            raise ValueError("cnpj já cadastrado")

        except Exception as e:
            self.db.rollback()
            raise e

    def update_custos_anuais(self, custo_anual_id, data, dados_token):
        try:
            data['log_id'] = dados_token['dados']['id']
            custo_anual = self.db.query(CustosAnuais).filter(
                CustosAnuais.id == custo_anual_id
            ).first()
            if not custo_anual:
                raise ValueError("Custo não encontrado")

            campos_para_remover = ["frota_id"]
            dados_custo_anual = remove_campos(data, campos_para_remover)

            for campo, valor in dados_custo_anual.items():
                setattr(custo_anual, campo, valor)
                
            self.db.commit()
            self.db.refresh(custo_anual)

            return custo_anual

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_custos_anuais(self, custo_anual_id):
        try:
            custo_anual = self.db.query(CustosAnuais).filter(
                CustosAnuais.id == custo_anual_id
            ).first()
            if not custo_anual:
                raise ValueError("Custo não encontrado")

            self.db.delete(custo_anual)
            self.db.commit()

            return {"message": "Custo removido com sucesso"}

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_custos_anuais(self, custo_anual_id, ativa, dados_token):
        try:
            log_id = dados_token['dados']['id']
            custo_anual = self.db.query(CustosAnuais).filter(
                CustosAnuais.id == custo_anual_id
            ).first()
            if not custo_anual:
                raise ValueError("Custo não encontrado")

            if ativa == 2:
                custo_anual.deleted_at = func.now()

            elif ativa == 1:
                custo_anual.deleted_at = None

            custo_anual.status_id = ativa
            custo_anual.log_id = log_id

            self.db.commit()
            self.db.refresh(custo_anual)

            return custo_anual

        except Exception as e:
            self.db.rollback()
            raise e

    def listar_custos_anuais(self, dados_token, filtro):
        try:
            dados = dados_token['dados']
            parametros = ["franquia_id","franquiado_id","locatarios_id"]

            filtro_token = filtro_basico(FranquiaFraqueadoLocatario, dados, parametros)
            Status = aliased(Codigo, name="status")

            query = (
                self.db.query(CustosAnuais, Frota, Status, User)
                .join(
                    Frota,
                    Frota.id == CustosAnuais.frota_id
                )
                .join(
                    Locatario,
                    Locatario.frota_id == CustosAnuais.frota_id
                )
                .outerjoin(
                    FranquiaFraqueadoLocatario,
                    and_(
                        FranquiaFraqueadoLocatario.franquiado_id == Frota.fraqueado_id,
                        FranquiaFraqueadoLocatario.locatarios_id == Locatario.id,
                    )
                )
                .outerjoin(
                    Status, 
                    and_(
                        Status.depara_id == 9,
                        Status.codigo == CustosAnuais.status_id
                    )
                )
                .outerjoin(
                    User,
                    User.id == CustosAnuais.log_id
                )
            )
            query = filtros_basicos_custos_anuais(query, filtro)
            custo_anuais = query.filter(*filtro_token).all()
            saida = []
            for custo_anual, frota, status, user in custo_anuais:
                item = {**custo_anual.__dict__}
                item['placa'] = formatar_placa(frota.placa) if frota else None
                item["status"] = status.descricao if status else None
                item["usuario"] = user.nome if user else None
                saida.append(item)

            # sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
            # return {"sql": filtro}
            return saida

        except Exception as e:
            self.db.rollback()
            raise e