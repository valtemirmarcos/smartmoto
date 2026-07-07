from sqlalchemy.orm import Session, aliased
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, extract, or_, and_
from decimal import Decimal

from models.Faturamento import Faturamento
from models.Semanal import Semanal
from models.FranquiaFraqueadoLocatario import FranquiaFraqueadoLocatario
from models.Oficina import Oficina
from models.DespesaFixa import DespesaFixa
from models.Despesa import Despesa
from models.Frota import Frota
from models.Locatario import Locatario
from models.Codigo import Codigo
from models.User import User

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios, calcular_data_pagamento, formatar_placa

import os
import re
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from config.filtros import filtro_basico_token, filtros_basicos_faturamentos

class FaturamentosRepository:
    def __init__(self, db: Session):
        self.db = db


    def create_faturamentos(self, data, dados_token):

        campos_obrigatorios = [
            "franquia_franquiador_locatario_id",
            "mes",
            "ano",
            "valor_entrada",
            "valor_saida",
            "data_pagamento",
            "tipo_pagamento_id",
            "status_id"
        ]
        saida = validar_campos_obrigatorios(campos_obrigatorios, data)

        data['log_id'] = dados_token['dados']['id']
        dados_faturamentos = data
        try:

            faturamento = Faturamento(**dados_faturamentos)
            self.db.add(faturamento)
            self.db.commit()
            self.db.refresh(faturamento)
            return faturamento
        

        except Exception as e:
            self.db.rollback()
            raise e

    def update_faturamentos(self, faturamento_id, data, dados_token):
        try:
            data['log_id'] = dados_token['dados']['id']
            faturamento = self.db.query(Faturamento).filter(
                Faturamento.id == faturamento_id
            ).first()
            if not faturamento:
                raise ValueError("faturamento não encontrada")

            campos_para_remover = ["franquia_franquiador_locatario_id"]
            dados_faturamento = remove_campos(data, campos_para_remover)
            for campo, valor in dados_faturamento.items():
                setattr(faturamento, campo, valor)
            self.db.commit()
            self.db.refresh(faturamento)

            return faturamento

        except Exception as e:
            self.db.rollback()
            raise e

    def delete_faturamentos(self, faturamento_id):
        try:
            faturamento = self.db.query(Faturamento).filter(
                Faturamento.id == faturamento_id
            ).first()
            if not faturamento:
                raise ValueError("faturamento não encontrada")

            self.db.delete(faturamento)
            self.db.commit()

            return {"message": "Faturamento removida com sucesso"}

        except Exception as e:
            self.db.rollback()
            raise e

    def sfdelete_faturamentos(self, faturamento_id, ativa, dados_token):
        try:
            log_id = dados_token['dados']['id']
            faturamento = self.db.query(Faturamento).filter(
                Faturamento.id == faturamento_id
            ).first()
            if not faturamento:
                raise ValueError("faturamento não encontrada")

            if ativa == 2:
                faturamento.deleted_at = func.now()

            elif ativa == 1:
                faturamento.deleted_at = None

            faturamento.status_id = ativa
            faturamento.log_id = log_id

            self.db.commit()
            self.db.refresh(faturamento)

            return faturamento

        except Exception as e:
            self.db.rollback()
            raise e

    def gerarFatura(self, franquiado_id, mes, ano, dados_token, royaties=None):
        try:
            log_id = dados_token['dados']['id']
            codigo = (
                self.db.query(FranquiaFraqueadoLocatario.id)
                .filter(
                    FranquiaFraqueadoLocatario.franquiado_id == franquiado_id,
                    FranquiaFraqueadoLocatario.locatarios_id == None
                )
                .scalar()
            )
            despesas = []
            faturamento_bruto = self.somar_faturamento_bruto(franquiado_id, mes, ano)
            gasto_oficina = self.somar_gastos_oficina(franquiado_id, mes, ano)
            despesas_fixas = self.somar_despesas_fixas(franquiado_id)

            valor_royaties = 0
            if royaties is not None:
                royaties = Decimal(str(royaties))
                valor_royaties = faturamento_bruto * (royaties / Decimal("100"))
            total = faturamento_bruto-(gasto_oficina+despesas_fixas+valor_royaties)
            vlsaida = gasto_oficina+despesas_fixas+valor_royaties 
            dados_faturamentos = {
                "franquia_franquiador_locatario_id":codigo,
                "mes":mes,
                "ano":ano,
                "valor_entrada":faturamento_bruto,
                "valor_saida":vlsaida,
                "data_pagamento":calcular_data_pagamento(10),
                "tipo_pagamento_id":1,
                "status_id":1,
                "log_id": log_id
            }
            faturamento = (
                self.db.query(Faturamento)
                .filter(
                    Faturamento.mes == mes,
                    Faturamento.ano == ano,
                    Faturamento.deleted_at.is_(None),
                    Faturamento.tipo_pagamento_id == 1,
                    Faturamento.franquia_franquiador_locatario_id == codigo
                ).first()
            )
            
            if faturamento is None:
                faturamento = Faturamento(**dados_faturamentos)
                self.db.add(faturamento)
            else:
                campos_para_remover = ["franquia_franquiador_locatario_id"]
                update_faturamento = remove_campos(dados_faturamentos, campos_para_remover)
                for campo, valor in update_faturamento.items():
                    setattr(faturamento, campo, valor)

            self.db.commit()
            self.db.refresh(faturamento)
            
            jsonDespesas = {
                "franquia_franquiador_locatario_id":codigo,
                "franquiado_id":franquiado_id,
                "mes":mes,
                "ano":ano,
                "gasto_oficina":gasto_oficina,
                "valor_royaties":valor_royaties,
                "log_id": log_id
            }
            
        
            processar_despesas = self.processar_despesas(jsonDespesas)

            return {
                "faturamento": self.model_to_dict(faturamento),
                "despesas": processar_despesas
            }

            

        except Exception as e:
            self.db.rollback()
            raise e

    def somar_faturamento_bruto(self, franquiado_id, mes, ano):
        faturamento_bruto = (
            self.db.query(
                func.coalesce(func.sum(Semanal.valor_pago), 0).label("total")
            )
            .join(
                FranquiaFraqueadoLocatario,
                FranquiaFraqueadoLocatario.id == Semanal.franquia_franquiador_locatario_id
            )
            .filter(
                extract("month", Semanal.data_prevista) == int(mes),
                extract("year", Semanal.data_prevista) == int(ano),
                Semanal.status_id == 2,
                Semanal.deleted_at.is_(None),
                FranquiaFraqueadoLocatario.franquiado_id == franquiado_id
            )
            .scalar()
        )

        return faturamento_bruto

    def somar_gastos_oficina(self, franquiado_id, mes, ano):
        gasto_oficina = (
            self.db.query(
                func.coalesce(func.sum(Oficina.pagamento), 0).label("total")
            )
            .join(
                FranquiaFraqueadoLocatario,
                FranquiaFraqueadoLocatario.id == Oficina.franquia_franquiador_locatario_id
            )
            .filter(
                extract("month", Oficina.data_servico) == int(mes),
                extract("year", Oficina.data_servico) == int(ano),
                Oficina.deleted_at.is_(None),
                FranquiaFraqueadoLocatario.franquiado_id == franquiado_id
            )
            .scalar()
        )

        return gasto_oficina

    def somar_despesas_fixas(self, franquiado_id):
        despesas_fixas = (
            self.db.query(
                func.coalesce(func.sum(DespesaFixa.valor), 0).label("total")
            )   
            .join(
                FranquiaFraqueadoLocatario,
                FranquiaFraqueadoLocatario.id == DespesaFixa.franquia_franquiador_locatario_id
            )          
            .filter(
                DespesaFixa.deleted_at.is_(None),
                FranquiaFraqueadoLocatario.franquiado_id == franquiado_id 
            )
            .scalar()
        )


        return despesas_fixas

    def processar_despesas(self, jsonDados):
        franquiado_id = jsonDados['franquiado_id']
        log_id = jsonDados['log_id']
        despesas_fixas = (
            self.db.query(
                FranquiaFraqueadoLocatario.id,
                DespesaFixa.descricao,
                func.coalesce(func.sum(DespesaFixa.valor), 0).label("total")
            )   
            .join(
                FranquiaFraqueadoLocatario,
                FranquiaFraqueadoLocatario.id == DespesaFixa.franquia_franquiador_locatario_id
            )          
            .filter(
                DespesaFixa.deleted_at.is_(None),
                FranquiaFraqueadoLocatario.franquiado_id == franquiado_id 
            )
            .group_by(
                FranquiaFraqueadoLocatario.id,
                DespesaFixa.descricao
            )
            .all()
        )
        dados_despesas = []
        for franquia_franquiador_locatario_id, descricao, total in despesas_fixas:
            dados_despesas.append({
                "franquia_franquiador_locatario_id":franquia_franquiador_locatario_id,
                "despesa": descricao,
                "valor": float(total),
                "mes":jsonDados['mes'],
                "ano":jsonDados['ano'],
                "log_id": log_id,
            })
        
        if float(jsonDados['gasto_oficina']) > 0:
            dados_despesas.append({
                "franquia_franquiador_locatario_id":jsonDados['franquia_franquiador_locatario_id'],
                "despesa": "Oficina",
                "valor": float(jsonDados['gasto_oficina']),
                "mes":jsonDados['mes'],
                "ano":jsonDados['ano'],
                "log_id": log_id,
            })
        if float(jsonDados['valor_royaties']) > 0:
            dados_despesas.append({
                "franquia_franquiador_locatario_id":jsonDados['franquia_franquiador_locatario_id'],
                "despesa": "Royaties",
                "valor": float(jsonDados['valor_royaties']),
                "mes":jsonDados['mes'],
                "ano":jsonDados['ano'],
                "log_id": log_id,
            })

        # INSERT OU UPDATE
        for item in dados_despesas:

            despesa = (
                self.db.query(Despesa)
                .filter(
                    Despesa.ano == item["ano"],
                    Despesa.mes == item["mes"],
                    Despesa.despesa == item["despesa"],
                    Despesa.franquia_franquiador_locatario_id == item["franquia_franquiador_locatario_id"],
                    Despesa.deleted_at.is_(None)
                )
                .first()
            )

            if despesa is None:
                nova_despesa = Despesa(**item)
                self.db.add(nova_despesa)
            else:
                despesa.valor = item["valor"]

        self.db.commit()

        return dados_despesas

    def model_to_dict(self, obj):
        return {
            coluna.name: getattr(obj, coluna.name)
            for coluna in obj.__table__.columns
        }

    def baixa_calcao_faturamento(self, calcao):
        dados_faturamentos = []
        self.db.commit()
        self.db.refresh(calcao)
        agora = datetime.now()
        mes = agora.strftime("%m")   # Ex: "05"
        ano = agora.strftime("%Y")   # Ex: "2026"
        dados_faturamentos = {
            "franquia_franquiador_locatario_id":calcao.franquia_franquiador_locatario_id,
            "mes":int(mes),
            "ano":int(ano),
            "valor_entrada":calcao.valor,
            "valor_saida":0,
            "data_pagamento":agora.strftime("%Y-%m-%d"),
            "tipo_pagamento_id":2,
            "status_id":2,
            "frota_id":calcao.frota_id,
            "log_id":calcao.log_id
        }
        faturamento = (
            self.db.query(Faturamento)
            .filter(
                Faturamento.franquia_franquiador_locatario_id == calcao.franquia_franquiador_locatario_id, 
                Faturamento.frota_id == calcao.frota_id,
                Faturamento.tipo_pagamento_id == 2,
                Faturamento.mes == int(mes),
                Faturamento.ano == int(ano)
            )
            .first()
        )
        if faturamento is None:
            faturamento = Faturamento(**dados_faturamentos)
            self.db.add(faturamento)
            self.db.commit()
            self.db.refresh(faturamento)

    def listar_faturamentos(self, dados_token, filtro):
        try:
            franquiado_id = dados_token['dados']['franquiado_id']
            franquia_id = dados_token['dados']['franquia_id']
            locatario_id = dados_token['dados']['locatarios_id']

            if locatario_id is not None:
                return None

            Status = aliased(Codigo, name="status")
            FormaPgto = aliased(Codigo, name="forma_pgto")

            query = (
                self.db.query(Faturamento, Frota, FormaPgto, Status, User, Locatario)
                .outerjoin(
                    Frota,
                    Frota.id == Faturamento.frota_id
                )
                .outerjoin(
                    Locatario,
                    Locatario.frota_id == Faturamento.frota_id
                )
                .outerjoin(
                    Status, 
                    and_(
                        Status.depara_id == 7,
                        Status.codigo == Faturamento.status_id
                    )
                )
                .outerjoin(
                    FormaPgto, 
                    and_(
                        FormaPgto.depara_id == 8,
                        FormaPgto.codigo == Faturamento.tipo_pagamento_id
                    )
                )
                .outerjoin(
                    User,
                    User.id == Faturamento.log_id
                )
            )

            query = filtros_basicos_faturamentos(query, filtro)
            faturamentos = query.all()
            saida = []
            for faturamento, frota, status, formaPgto, user, locatario in faturamentos:
                item = {**faturamento.__dict__}
                item['placa'] = formatar_placa(frota.placa) if frota else None
                item["pagamento"] = formaPgto.descricao if formaPgto else None
                item["status"] = status.descricao if status else None
                item["usuario"] = user.nome if user else None
                item["locatario"] = locatario.nome if locatario else None
                saida.append(item)

            # sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))
            # return {"sql": filtro}
            return saida

        except Exception as e:
            self.db.rollback()
            raise e