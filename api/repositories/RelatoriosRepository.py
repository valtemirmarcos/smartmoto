from sqlalchemy.orm import Session, aliased
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_, and_, case
from datetime import date, timedelta
import traceback

from models.Multa import Multa
from models.Frota import Frota
from models.FranquiaFraqueadoLocatario import FranquiaFraqueadoLocatario
from models.Locatario import Locatario
from models.Codigo import Codigo
from models.User import User
from models.Semanal import Semanal
from models.Oficina import Oficina
from models.DespesaFixa import DespesaFixa
from models.Franqueado import Franqueado

from config.funcoes import remove_campos, apenasNumeros, valida_placa, validar_campos_obrigatorios, formatar_placa

import os
import re

from config.filtros import filtro_basico_token, filtros_basicos_multas

class RelatoriosRepository:
    def __init__(self, db: Session):
        self.db = db

    def dashboard(self, dados_token, filtro):
        
        try:
            dados = dados_token['dados']
            # return dados
            parametros = ["franquia_id","franquiado_id","locatarios_id"]
            hoje = date.today()
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            fim_semana = inicio_semana + timedelta(days=7)

            # Primeiro dia do mês atual
            mes_inicial = date(hoje.year, hoje.month, 1)

            # Primeiro dia do próximo mês
            if hoje.month == 12:
                mes_final = date(hoje.year + 1, 1, 1)
            else:
                mes_final = date(hoje.year, hoje.month + 1, 1)

            filtro_token = filtro_basico_token(FranquiaFraqueadoLocatario, dados, parametros)
            total_semanal = self.soma_totais_semanais(filtro_token, inicio_semana, fim_semana)
            total_mensal = self.soma_totais_semanais(filtro_token, mes_inicial, mes_final)
            multas_emAberto = self.multas_emAberto(filtro_token)
            status_frota = self.status_frota(dados)
            status_pgto_semanais = self.status_pgto_semanais(filtro_token, mes_inicial, mes_final)
            json = {
                "filtro_token":filtro_token,
                "inicio_semana":inicio_semana,
                "fim_semana":fim_semana,
                "mes_inicial": mes_inicial,
                "mes_final": mes_final
            }
            resumo_financeiro_frota = self.resumo_financeiro_frota(json)
            return {
                "total_semanal":total_semanal,
                "total_mensal":total_mensal,
                "multas_emAberto": multas_emAberto,
                "status_frota": status_frota,
                "status_pgto_semanais":status_pgto_semanais,
                "resumo_financeiro_frota": resumo_financeiro_frota
            }

        except Exception as e:
            self.db.rollback()
            raise e

    def soma_totais_semanais(self, filtro_token, data_inicial, data_final):
        total_pago = (
            self.db.query(func.sum(Semanal.valor_pago))
            .join(
                FranquiaFraqueadoLocatario,
                FranquiaFraqueadoLocatario.id == Semanal.franquia_franquiador_locatario_id
            )
            .filter(
                Semanal.data_pagamento >= data_inicial,
                Semanal.data_pagamento <= data_final
            )
            .filter(*filtro_token)
            .scalar()
        )

        return total_pago or 0

    def multas_emAberto(self, filtro_token):
        total_multas = (
            self.db.query(func.count(Multa.id))
            .join(
                FranquiaFraqueadoLocatario,
                FranquiaFraqueadoLocatario.id == Multa.franquia_franquiador_locatario_id
            )
            .filter(Multa.status_id.in_([1, 2]))
            .filter(*filtro_token)
            .scalar()
        )

        return total_multas or 0

    def status_frota(self, dados):
        tipo_acesso = dados.get("tipoAcessoID")
        resultado = (
            self.db.query(
                Frota.status_id,
                Codigo.descricao.label("status_descricao"),
                func.count(Frota.id).label("quantidade")
            )
            .outerjoin(
                Locatario,
                and_(
                    Locatario.frota_id == Frota.id,
                    Locatario.status_id == 1
                ) 
                
            )
            .outerjoin(
                Codigo, 
                and_(
                    Codigo.depara_id == 2,
                    Codigo.codigo == Frota.status_id
                )
            )
            .group_by(Frota.status_id, Codigo.descricao)
        )
        if tipo_acesso == 3:
            resultado = resultado.filter(Locatario.id == dados.get("locatarios_id"))
        elif tipo_acesso == 2:
            resultado = resultado.filter(Frota.fraqueado_id == dados.get("franquiado_id"))
        elif tipo_acesso == 1:
            pass
        resultado = resultado.all()
        # Status fixos
        queryCodigo = (
            self.db.query(Codigo)
            .filter(
                Codigo.depara_id == 2
            )
            .all()
        )
        retorno = {}

        for dado in queryCodigo:
            retorno[dado.codigo] = {
                "status_id": dado.codigo,
                "status": dado.descricao,
                "quantidade": 0
            }

        # Atualiza com os valores encontrados
        for r in resultado:
            retorno[r.status_id] = {
                "status_id": r.status_id,
                "status": r.status_descricao,
                "quantidade": r.quantidade
            }

        return list(retorno.values())

    def status_pgto_semanais(self, filtro_token, data_inicial, data_final):
        Status = aliased(Codigo, name="status")
        query = (
            self.db.query(
                Semanal.status_id,
                Status.descricao.label("status_descricao"),
                func.count(Semanal.id).label("quantidade")
            )
            .join(
                FranquiaFraqueadoLocatario,
                FranquiaFraqueadoLocatario.id == Semanal.franquia_franquiador_locatario_id
            )
            .outerjoin(
                Status, 
                and_(
                    Status.depara_id == 3,
                    Status.codigo == Semanal.status_id
                )
            )
            .filter(
                Semanal.data_prevista >= data_inicial,
                Semanal.data_prevista <= data_final
            )
            .filter(*filtro_token)
            .group_by(Semanal.status_id, Status.descricao)
            
        )
        query = query.all()
        queryCodigo = (
            self.db.query(Codigo)
            .filter(
                Codigo.depara_id == 3
            )
            .all()
        )
        retorno = {}

        for dado in queryCodigo:
            retorno[dado.codigo] = {
                "status_id": dado.codigo,
                "status": dado.descricao,
                "quantidade": 0,
                "cor": dado.cor
            }
        # Atualiza com os valores encontrados
        for r in query:
            retorno[r.status_id]["status"] = r.status_descricao
            retorno[r.status_id]["quantidade"] = r.quantidade

        return list(retorno.values())

    def resumo_financeiro_frota(self, json):
        print("ANTES DA QUERY")
        try:
            filtro_token = json['filtro_token']
            inicio_semana = json['inicio_semana']
            fim_semana = json['fim_semana']
            mes_inicial = json['mes_inicial']
            mes_final = json['mes_final']

            frotaStatus = aliased(Codigo)
            codigoStatus = aliased(Codigo)

            # Total semanal
            sub_total_semanal = (
                self.db.query(
                    Semanal.frota_id.label("frota_id"),
                    func.sum(Semanal.valor_pago).label("total_semanal")
                )
                .filter(
                    Semanal.data_pagamento >= inicio_semana,
                    Semanal.data_pagamento <= fim_semana
                )
                .group_by(Semanal.frota_id)
                .subquery()
            )

            # Total mensal
            sub_total_mensal = (
                self.db.query(
                    Semanal.frota_id.label("frota_id"),
                    func.sum(Semanal.valor_pago).label("total_mensal")
                )
                .filter(
                    Semanal.data_pagamento >= mes_inicial,
                    Semanal.data_pagamento <= mes_final
                )
                .group_by(Semanal.frota_id)
                .subquery()
            )

            # Último status (igual ao seu MAX(descricao))
            sub_ultimo_status = (
                self.db.query(
                    Semanal.frota_id.label("frota_id"),
                    func.max(codigoStatus.descricao).label("ultimo_status")
                )
                .join(
                    codigoStatus,
                    and_(
                        codigoStatus.codigo == Semanal.status_id,
                        codigoStatus.depara_id == 3
                    )
                )
                .group_by(Semanal.frota_id)
                .subquery()
            )

            query = (
                self.db.query(
                    Frota.placa,
                    func.coalesce(sub_total_semanal.c.total_semanal, 0).label("totalSemanal"),
                    func.coalesce(sub_total_mensal.c.total_mensal, 0).label("totalMensal"),
                    func.coalesce(sub_ultimo_status.c.ultimo_status, "Sem Status").label("ultimoStatus"),
                    frotaStatus.descricao.label("statusFrota")
                )
                .outerjoin(
                    sub_total_semanal,
                    sub_total_semanal.c.frota_id == Frota.id
                )
                .outerjoin(
                    sub_total_mensal,
                    sub_total_mensal.c.frota_id == Frota.id
                )
                .outerjoin(
                    sub_ultimo_status,
                    sub_ultimo_status.c.frota_id == Frota.id
                )
                .outerjoin(
                    frotaStatus,
                    and_(
                        frotaStatus.codigo == Frota.status_id,
                        frotaStatus.depara_id == 2
                    )
                )
            )

            resultado = query.all()
            return [dict(r._mapping) for r in resultado]
        except Exception:
            # return traceback.format_exc()
            return "falha ao gerar resumo financeiro"

    def custos(self, dados_token, filtro):
        try:
            dados = dados_token['dados']
            sub_oficina = (
                self.db.query(
                    FranquiaFraqueadoLocatario.franquiado_id.label("franquiado_id"),
                    func.sum(Oficina.valor).label("valor_oficina"),
                    func.year(Oficina.data_servico).label("ano"),
                    func.month(Oficina.data_servico).label("mes"),
                )
                .join(
                    FranquiaFraqueadoLocatario,
                    Oficina.franquia_franquiador_locatario_id == FranquiaFraqueadoLocatario.id,
                )
                .group_by(
                    FranquiaFraqueadoLocatario.franquiado_id,
                    func.year(Oficina.data_servico),
                    func.month(Oficina.data_servico),
                )
            ).subquery()

            sub_despesas = (
                self.db.query(
                    FranquiaFraqueadoLocatario.franquiado_id.label("franquiado_id"),
                    func.sum(
                        case(
                            (DespesaFixa.descricao == "Seguro", DespesaFixa.valor),
                            else_=0,
                        )
                    ).label("seguro"),
                    func.sum(
                        case(
                            (DespesaFixa.descricao == "Rastreador", DespesaFixa.valor),
                            else_=0,
                        )
                    ).label("rastreador"),
                )
                .join(
                    FranquiaFraqueadoLocatario,
                    DespesaFixa.franquia_franquiador_locatario_id == FranquiaFraqueadoLocatario.id,
                )
                .group_by(FranquiaFraqueadoLocatario.franquiado_id)
            ).subquery()

            # Consulta principal
            query = (
                self.db.query(
                    FranquiaFraqueadoLocatario.franquiado_id.label("franquiado_id"),
                    Franqueado.nome.label("nome"),
                    func.date_format(Semanal.data_pagamento, "%m/%y").label("periodo"),
                    (func.sum(Semanal.valor_pago) * 0.1).label("royaties"),
                    (func.sum(Semanal.valor_pago)).label("bruto"),
                    sub_despesas.c.seguro,
                    sub_despesas.c.rastreador,
                    func.coalesce(sub_oficina.c.valor_oficina, 0).label("manutencao"),
                    (
                        func.coalesce(func.sum(Semanal.valor_pago) * 0.1, 0)
                        + func.coalesce(sub_oficina.c.valor_oficina, 0)
                        + func.coalesce(sub_despesas.c.seguro, 0)
                        + func.coalesce(sub_despesas.c.rastreador, 0)
                    ).label("total"),
                    (
                        func.sum(Semanal.valor_pago) - (
                            func.coalesce(func.sum(Semanal.valor_pago) * 0.1, 0)
                            + func.coalesce(sub_oficina.c.valor_oficina, 0)
                            + func.coalesce(sub_despesas.c.seguro, 0)
                            + func.coalesce(sub_despesas.c.rastreador, 0)
                        )

                    ).label("liquido"),
                )
                .join(
                    FranquiaFraqueadoLocatario,
                    Semanal.franquia_franquiador_locatario_id
                    == FranquiaFraqueadoLocatario.id,
                )
                .join(
                    Franqueado,
                    FranquiaFraqueadoLocatario.franquiado_id == Franqueado.id,
                )
                .outerjoin(
                    sub_oficina,
                    and_(
                        sub_oficina.c.franquiado_id == Franqueado.id,
                        sub_oficina.c.ano == func.year(Semanal.data_pagamento),
                        sub_oficina.c.mes == func.month(Semanal.data_pagamento),
                    ),
                )
                .outerjoin(
                    sub_despesas,
                    sub_despesas.c.franquiado_id == Franqueado.id,
                )
                .filter(
                    Semanal.data_pagamento >= filtro['dataInicio'],
                    Semanal.data_pagamento <= filtro['dataFim'],
                )
                .filter(
                    Semanal.deleted_at.is_(None)
                )
                .group_by(
                    FranquiaFraqueadoLocatario.franquiado_id,
                    Franqueado.nome,
                    func.date_format(Semanal.data_pagamento, "%m/%y"),
                    sub_despesas.c.seguro,
                    sub_despesas.c.rastreador,
                    sub_oficina.c.valor_oficina,
                )
            )

            resultado = query.all()
            return [dict(r._mapping) for r in resultado]

        except Exception as e:
            traceback.print_exc()
            raise

    def custo_moto(self, dados_token, filtro):
        try:
            dados = dados_token['dados']
            sub_despesas = (
                self.db.query(
                    FranquiaFraqueadoLocatario.franquiado_id.label("franquiado_id"),
                    DespesaFixa.frota_id.label("frota_id"),
                    func.sum(
                        case(
                            (DespesaFixa.descricao == "Seguro", DespesaFixa.valor),
                            else_=0
                        )
                    ).label("seguro"),
                    func.sum(
                        case(
                            (DespesaFixa.descricao == "Rastreador", DespesaFixa.valor),
                            else_=0
                        )
                    ).label("rastreador"),
                )
                .join(
                    FranquiaFraqueadoLocatario,
                    DespesaFixa.franquia_franquiador_locatario_id == FranquiaFraqueadoLocatario.id,
                )
                .join(
                    Frota,
                    DespesaFixa.frota_id == Frota.id,
                )
                .group_by(
                    FranquiaFraqueadoLocatario.franquiado_id,
                    DespesaFixa.frota_id,
                )
            ).subquery()

            # ==========================
            # Subquery Oficina
            # ==========================
            sub_oficina = (
                self.db.query(
                    FranquiaFraqueadoLocatario.franquiado_id.label("franquiado_id"),
                    Oficina.frota_id.label("frota_id"),
                    func.sum(Oficina.valor).label("valor_oficina"),
                    func.year(Oficina.data_servico).label("ano"),
                    func.month(Oficina.data_servico).label("mes"),
                )
                .join(
                    FranquiaFraqueadoLocatario,
                    Oficina.franquia_franquiador_locatario_id == FranquiaFraqueadoLocatario.id,
                )
                .group_by(
                    FranquiaFraqueadoLocatario.franquiado_id,
                    Oficina.frota_id,
                    func.year(Oficina.data_servico),
                    func.month(Oficina.data_servico),
                )
            ).subquery()

            # ==========================
            # Consulta Principal
            # ==========================
            query = (
                self.db.query(
                    Franqueado.nome.label("franqueado"),

                    func.date_format(
                        Semanal.data_pagamento,
                        "%m/%y"
                    ).label("periodo"),

                    Frota.id.label("frota_id"),
                    Frota.placa,

                    func.coalesce(
                        func.sum(Semanal.valor_pago),
                        0
                    ).label("valores_semanais"),

                    func.coalesce(
                        func.sum(Semanal.valor_pago) * 0.1,
                        0
                    ).label("royalties"),

                    func.coalesce(
                        sub_despesas.c.seguro,
                        0
                    ).label("seguro"),

                    func.coalesce(
                        sub_despesas.c.rastreador,
                        0
                    ).label("rastreador"),

                    func.coalesce(
                        sub_oficina.c.valor_oficina,
                        0
                    ).label("valor_oficina"),

                    (
                        func.coalesce(func.sum(Semanal.valor_pago) * 0.1, 0)
                        + func.coalesce(sub_despesas.c.seguro, 0)
                        + func.coalesce(sub_despesas.c.rastreador, 0)
                        + func.coalesce(sub_oficina.c.valor_oficina, 0)
                    ).label("total"),
                    (
                        (func.coalesce(func.sum(Semanal.valor_pago), 0))-(
                            func.coalesce(func.sum(Semanal.valor_pago) * 0.1, 0)
                        + func.coalesce(sub_despesas.c.seguro, 0)
                        + func.coalesce(sub_despesas.c.rastreador, 0)
                        + func.coalesce(sub_oficina.c.valor_oficina, 0)
                        )

                    ).label("liquido"),
                )

                .join(
                    FranquiaFraqueadoLocatario,
                    Semanal.franquia_franquiador_locatario_id == FranquiaFraqueadoLocatario.id,
                )

                .join(
                    Franqueado,
                    FranquiaFraqueadoLocatario.franquiado_id == Franqueado.id,
                )

                .join(
                    Frota,
                    Semanal.frota_id == Frota.id,
                )

                .outerjoin(
                    sub_despesas,
                    and_(
                        sub_despesas.c.franquiado_id == Franqueado.id,
                        sub_despesas.c.frota_id == Semanal.frota_id,
                    ),
                )

                .outerjoin(
                    sub_oficina,
                    and_(
                        sub_oficina.c.franquiado_id == Franqueado.id,
                        sub_oficina.c.frota_id == Semanal.frota_id,
                        sub_oficina.c.ano == func.year(Semanal.data_pagamento),
                        sub_oficina.c.mes == func.month(Semanal.data_pagamento),
                    ),
                )

                .filter(
                    Semanal.data_pagamento >= filtro['dataInicio'],
                    Semanal.data_pagamento <= filtro['dataFim'],
                )
                .filter(
                    Semanal.deleted_at.is_(None)
                )

                .group_by(
                    Franqueado.nome,
                    func.date_format(Semanal.data_pagamento, "%m/%y"),
                    Frota.id,
                    Frota.placa,
                    sub_despesas.c.seguro,
                    sub_despesas.c.rastreador,
                    sub_oficina.c.valor_oficina,
                )
            )

            resultado = query.all()
            return [dict(r._mapping) for r in resultado]

        except Exception as e:
            traceback.print_exc()
            raise

    def lucro_moto(self, dados_token, filtro):
        try:
            dados = dados_token['dados']
            sub_despesas = (
                self.db.query(
                    FranquiaFraqueadoLocatario.franquiado_id.label("franquiado_id"),
                    DespesaFixa.frota_id.label("frota_id"),
                    func.sum(
                        case(
                            (DespesaFixa.descricao == "Seguro", DespesaFixa.valor),
                            else_=0
                        )
                    ).label("seguro"),
                    func.sum(
                        case(
                            (DespesaFixa.descricao == "Rastreador", DespesaFixa.valor),
                            else_=0
                        )
                    ).label("rastreador"),
                )
                .join(
                    FranquiaFraqueadoLocatario,
                    DespesaFixa.franquia_franquiador_locatario_id == FranquiaFraqueadoLocatario.id,
                )
                .join(
                    Frota,
                    DespesaFixa.frota_id == Frota.id,
                )
                .group_by(
                    FranquiaFraqueadoLocatario.franquiado_id,
                    DespesaFixa.frota_id,
                )
            ).subquery()

            # ==========================
            # Subquery Oficina
            # ==========================
            sub_oficina = (
                self.db.query(
                    FranquiaFraqueadoLocatario.franquiado_id.label("franquiado_id"),
                    Oficina.frota_id.label("frota_id"),
                    func.sum(Oficina.valor).label("valor_oficina"),
                    func.year(Oficina.data_servico).label("ano"),
                    func.month(Oficina.data_servico).label("mes"),
                )
                .join(
                    FranquiaFraqueadoLocatario,
                    Oficina.franquia_franquiador_locatario_id == FranquiaFraqueadoLocatario.id,
                )
                .group_by(
                    FranquiaFraqueadoLocatario.franquiado_id,
                    Oficina.frota_id,
                    func.year(Oficina.data_servico),
                    func.month(Oficina.data_servico),
                )
            ).subquery()

            total_mes = func.sum(
                func.sum(Semanal.valor_pago)
            ).over(
                partition_by=func.date_format(Semanal.data_pagamento, "%m/%y")
            )
            # ==========================
            # Consulta Principal
            # ==========================
            query = (
                self.db.query(
                    Franqueado.nome.label("franqueado"),

                    func.date_format(
                        Semanal.data_pagamento,
                        "%m/%y"
                    ).label("periodo"),

                    Frota.id.label("frota_id"),
                    Frota.placa,

                    func.coalesce(
                        func.sum(Semanal.valor_pago),
                        0
                    ).label("valores_semanais"),
                    (
                        func.coalesce(
                            func.sum(Semanal.valor_pago),
                            0
                        )-(
                            func.coalesce(func.sum(Semanal.valor_pago) * 0.1, 0)
                            + func.coalesce(sub_despesas.c.seguro, 0)
                            + func.coalesce(sub_despesas.c.rastreador, 0)
                            + func.coalesce(sub_oficina.c.valor_oficina, 0)
                        )

                    ).label("liquido"),
                    func.round(
                        (
                            func.coalesce(
                                func.sum(Semanal.valor_pago),
                                0
                            ) / total_mes
                        ) * 100,
                        2
                    ).label("percentual_mes"),
                )

                .join(
                    FranquiaFraqueadoLocatario,
                    Semanal.franquia_franquiador_locatario_id == FranquiaFraqueadoLocatario.id,
                )

                .join(
                    Franqueado,
                    FranquiaFraqueadoLocatario.franquiado_id == Franqueado.id,
                )

                .join(
                    Frota,
                    Semanal.frota_id == Frota.id,
                )

                .outerjoin(
                    sub_despesas,
                    and_(
                        sub_despesas.c.franquiado_id == Franqueado.id,
                        sub_despesas.c.frota_id == Semanal.frota_id,
                    ),
                )

                .outerjoin(
                    sub_oficina,
                    and_(
                        sub_oficina.c.franquiado_id == Franqueado.id,
                        sub_oficina.c.frota_id == Semanal.frota_id,
                        sub_oficina.c.ano == func.year(Semanal.data_pagamento),
                        sub_oficina.c.mes == func.month(Semanal.data_pagamento),
                    ),
                )

                .filter(
                    Semanal.data_pagamento >= filtro['dataInicio'],
                    Semanal.data_pagamento <= filtro['dataFim'],
                )
                .filter(
                    Semanal.deleted_at.is_(None)
                )

                .group_by(
                    Franqueado.nome,
                    func.date_format(Semanal.data_pagamento, "%m/%y"),
                    Frota.id,
                    Frota.placa,
                    sub_despesas.c.seguro,
                    sub_despesas.c.rastreador,
                    sub_oficina.c.valor_oficina,
                )
            )

            resultado = query.all()
            return [dict(r._mapping) for r in resultado]

        except Exception as e:
            traceback.print_exc()
            raise