from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_, and_
from models.Despesa import Despesa
from models.Franqueado import Franqueado
from models.User import User
from models.FranquiaFraqueadoLocatario import FranquiaFraqueadoLocatario


from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios
from config.filtros import filtros_basicos_despesas
import os
import re


class DespesasRepository:
    def __init__(self, db: Session):
        self.db = db



    def create_despesas(self, data, dados_token):

        campos_obrigatorios = [
            "franquia_franquiador_locatario_id",
            "valor",
            "mes",
            "ano",
            "despesa"
        ]
        saida = validar_campos_obrigatorios(campos_obrigatorios, data)
        data['log_id'] = dados_token['dados']['id']
        dados_despesas = data
        try:

            despesa = Despesa(**dados_despesas)
            self.db.add(despesa)
            self.db.commit()
            self.db.refresh(despesa)
            return despesa
        

        except Exception as e:
            self.db.rollback()
            raise e

    def update_despesas(self, despesa_id, data, dados_token):
        try:
            data['log_id'] = dados_token['dados']['id']
            despesa = self.db.query(Despesa).filter(
                Despesa.id == despesa_id
            ).first()
            if not despesa:
                raise ValueError("despesa não encontrada")

            campos_para_remover = ["franquia_franquiador_locatario_id", "frota_id"]
            dados_despesa = remove_campos(data, campos_para_remover)

            for campo, valor in dados_despesa.items():
                setattr(despesa, campo, valor)
                
            self.db.commit()
            self.db.refresh(despesa)

            return despesa

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_despesas(self, despesa_id):
        try:
            despesa = self.db.query(Despesa).filter(
                Despesa.id == despesa_id
            ).first()
            if not despesa:
                raise ValueError("despesa não encontrada")

            self.db.delete(despesa)
            self.db.commit()

            return {"message": "Despesa removida com sucesso"}

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_despesas(self, despesa_id, ativa, dados_token):
        try:
            log_id = dados_token['dados']['id']
            despesa = self.db.query(Despesa).filter(
                Despesa.id == despesa_id
            ).first()
            if not despesa:
                raise ValueError("despesa não encontrada")

            if ativa == 0:
                despesa.deleted_at = func.now()

            elif ativa == 1:
                despesa.deleted_at = None

            despesa.log_id = log_id

            self.db.commit()
            self.db.refresh(despesa)

            return despesa

        except Exception as e:
            self.db.rollback()
            raise e

    def listar_despesas(self, dados_token, filtro):
        try:
            # return dados_token
            franquiado_id = dados_token['dados']['franquiado_id']
            franquia_id = dados_token['dados']['franquia_id']
            locatario_id = dados_token['dados']['locatarios_id']

            if locatario_id is not None:
                return None

            query = (
                self.db.query(Despesa, User)
                .select_from(Despesa)
                .join(
                    Franqueado,
                    Franqueado.id == franquiado_id
                )
                .join(
                    FranquiaFraqueadoLocatario,
                    and_(
                        FranquiaFraqueadoLocatario.franquiado_id == franquiado_id,
                        FranquiaFraqueadoLocatario.franquia_id == franquia_id,
                    )
                )
                .outerjoin(
                    User,
                    User.id == Despesa.log_id
                )
            )
            query = filtros_basicos_despesas(query, filtro)
            despesas = query.all()
            saida = []
            for despesa, user in despesas:
                item = {**despesa.__dict__}
                item["usuario"] = user.nome if user else None
                saida.append(item)

            # sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
            # return {"sql": filtro}
            return saida

        except Exception as e:
            self.db.rollback()
            raise e