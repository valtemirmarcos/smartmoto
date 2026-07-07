from sqlalchemy.orm import Session, aliased
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_, and_

from models.Calcao import Calcao
from models.Faturamento import Faturamento
from models.Frota import Frota
from models.Franqueado import Franqueado
from models.FranquiaFraqueadoLocatario import FranquiaFraqueadoLocatario
from models.Locatario import Locatario
from models.Codigo import Codigo
from models.User import User

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios, filtro_basico, formatar_placa

import os
import re
from datetime import datetime
from repositories.FaturamentosRepository import FaturamentosRepository
from config.filtros import filtros_basicos_calcoes

class CalcoesRepository:
    def __init__(self, db: Session):
        self.db = db


    def create_calcoes(self, data, dados_token):

        campos_obrigatorios = [
            "franquia_franquiador_locatario_id",
            "frota_id",
            "data_deposito",
            "forma_pagamento_id",
            "valor",
            "valor_atual",
            "status_id"
        ]
        saida = validar_campos_obrigatorios(campos_obrigatorios, data)

        dados_calcoes = data
        dados_calcoes['log_id'] = dados_token['dados']['id']
        try:

            calcao = Calcao(**dados_calcoes)
            self.db.add(calcao)
            self.db.commit()
            self.db.refresh(calcao)
            return calcao
    
        except Exception as e:
            self.db.rollback()
            raise e

    def update_calcoes(self, calcao_id, data, dados_token):
        try:
            calcao = self.db.query(Calcao).filter(
                Calcao.id == calcao_id
            ).first()
            if not calcao:
                raise ValueError("calcao não encontrado")

            campos_para_remover = ["franquia_franquiador_locatario_id", "frota_id"]
            dados_calcao = remove_campos(data, campos_para_remover)
            dados_calcao['log_id'] = dados_token['dados']['id']


            if data['status_id'] == 2:
                calcao.deleted_at = func.now()
                calcao.status_id = 2
                calcao.valor_atual = 0
                
            for campo, valor in dados_calcao.items():
                setattr(calcao, campo, valor)
            self.db.commit()
            self.db.refresh(calcao)

            return calcao

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_calcoes(self, calcao_id, data):
        try:
            calcao = self.db.query(Calcao).filter(
                Calcao.id == calcao_id
            ).first()
            if not calcao:
                raise ValueError("calcao não encontrado")

            self.db.delete(calcao)
            self.db.commit()

            return {"message": "Calcao removido com sucesso"}

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_calcoes(self, calcao_id, ativa, dados_token):
        try:
            calcao = self.db.query(Calcao).filter(
                Calcao.id == calcao_id
            ).first()
            if not calcao:
                raise ValueError("calcao não encontrado")

            if ativa == 0:
                calcao.deleted_at = func.now()
                calcao.status_id = 0

            elif ativa == 1:
                calcao.deleted_at = None

            elif ativa == 2:
                # calcao.deleted_at = func.now()
                calcao.status_id = 2
                calcao.valor_atual = 0

            calcao.log_id = dados_token['dados']['id']

            self.db.commit()
            self.db.refresh(calcao)

            return calcao

        except Exception as e:
            self.db.rollback()
            raise e

    def baixar_calcao(self, frota_id, dados_token):
        try:
            log_id = dados_token['dados']['id']
            calcao = self.db.query(Calcao).filter(
                Calcao.frota_id == frota_id,
                Calcao.deleted_at == None
            ).first()
            if not calcao:
                raise ValueError("calcao não encontrado")

            # calcao.deleted_at = func.now()
            calcao.status_id = 2
            calcao.valor_atual = 0
            calcao.log_id = log_id

            self.db.commit()
            self.db.refresh(calcao)

            faturamento_repo = FaturamentosRepository(self.db)
            faturamento_repo.baixa_calcao_faturamento(calcao)
                

        except Exception as e:
            self.db.rollback()
            raise e
        


    def listar_calcoes(self, dados_token, filtro):
        try:
            dados = dados_token['dados']
            parametros = ["franquia_id","franquiado_id","locatarios_id"]

            filtro_token = filtro_basico(FranquiaFraqueadoLocatario, dados, parametros)

            Status = aliased(Codigo, name="status")
            FormaPgto = aliased(Codigo, name="forma_pgto")

            query = (
                self.db.query(Calcao, Frota, Status, FormaPgto, User, Franqueado)
                .join(
                    Frota,
                    Frota.id == Calcao.frota_id
                )
                .join(
                    Locatario,
                    Locatario.frota_id == Calcao.frota_id
                )
                .join(
                    Franqueado,
                    Franqueado.id == Frota.fraqueado_id
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
                        Status.depara_id == 4,
                        Status.codigo == Calcao.status_id
                    )
                )
                .outerjoin(
                    FormaPgto, 
                    and_(
                        FormaPgto.depara_id == 5,
                        FormaPgto.codigo == Calcao.forma_pagamento_id
                    )
                )
                .outerjoin(
                    User,
                    User.id == Calcao.log_id
                )
            )
            
            query = filtros_basicos_calcoes(query, filtro)
            query = query.filter(Calcao.deleted_at == None)
            calcoes = query.filter(*filtro_token).all()
            saida = []
            for calcao, frota, status, formaPgto, user, franquiado in calcoes:
                item = {**calcao.__dict__}
                item['placa'] = frota.placa if frota else None
                item["pagamento"] = formaPgto.descricao if formaPgto else None
                item["status"] = status.descricao if status else None
                item["usuario"] = user.nome if user else None
                item['nome_franquiado'] = franquiado.nome if franquiado else None
                saida.append(item)

            # sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
            # return {"sql": filtro}
            return saida

        except Exception as e:
            self.db.rollback()
            raise e


