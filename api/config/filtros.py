from models.Franquia import Franquia
from models.Frota import Frota
from models.Locatario import Locatario
from models.Calcao import Calcao
from models.Semanal import Semanal
from models.CustosAnuais import CustosAnuais
from models.Despesa import Despesa
from models.Multa import Multa
from models.Faturamento import Faturamento
from models.Oficina import Oficina
from models.Anexo import Anexo

from config.funcoes import apenasNumeros

def filtro_basico_token(modelo, dados: dict, campos: list = None) -> list:
    filtros = []
    for campo, valor in dados.items():
        if campos and campo not in campos:  # ignora se não estiver na lista
            continue
        if valor is not None:
            atributo = getattr(modelo, campo, None)
            if atributo is not None:
                filtros.append(atributo == valor)
    return filtros

def filtros_basicos_franquiado(query, filtro):
    if filtro['id'] is not None:
        query = query.filter(Franquia.id == filtro['id'])

    if filtro['status'] is not None:
        query = query.filter(Franquia.status_id == filtro['status'])

    return query

def filtros_basicos_frota(query, filtro):
    if filtro['id'] is not None:
        query = query.filter(Frota.id == filtro['id'])

    if filtro['status'] is not None:
        query = query.filter(Frota.status_id == filtro['status'])

    if filtro['franquiado'] is not None:
        query = query.filter(Frota.fraqueado_id == filtro['franquiado'])

    if filtro['placa'] is not None:
        query = query.filter(Frota.placa.like(f'%{filtro['placa']}%'))

    if filtro['cor'] is not None:
        query = query.filter(Frota.cor.like(f'%{filtro['cor']}%'))

    if filtro['ano'] is not None:
        query = query.filter(Frota.ano.like(f'%{filtro['ano']}%'))

    return query

def filtros_basicos_locatario(query, filtro):
    if filtro['id'] is not None:
        query = query.filter(Locatario.id == filtro['id'])

    if filtro['status'] is not None:
        query = query.filter(Locatario.status_id == filtro['status'])

    if filtro['placa'] is not None:
        query = query.filter(Locatario.frota_id == filtro['placa'])

    if filtro['plano'] is not None:
        query = query.filter(Locatario.plano_id == filtro['plano'])

    if filtro['nome'] is not None:
        query = query.filter(Locatario.nome.like(f'%{filtro['nome']}%'))

    if filtro['cpf'] is not None:
        cpf_limpo = apenasNumeros(filtro['cpf'])
        query = query.filter(Locatario.cpf.like(f'%{cpf_limpo}%'))

    if filtro['dataInicio'] is not None:
        query = query.filter(Locatario.data_inicio_contrato >= filtro['dataInicio'])

    if filtro['dataFim'] is not None:
        query = query.filter(Locatario.data_inicio_contrato <= filtro['dataFim'])

    if filtro['franquiado'] is not None:
        query = query.filter(Frota.fraqueado_id == filtro['franquiado'])
        
    return query

def filtros_basicos_calcoes(query, filtro):
    if filtro.get('id') is not None:
        query = query.filter(Calcao.id == filtro['id'])

    if filtro.get('status') is not None:
        query = query.filter(Calcao.status_id == filtro['status'])

    if filtro.get('placa') is not None:
        query = query.filter(Calcao.frota_id == filtro['placa'])

    if filtro.get('formaPagamento') is not None:
        query = query.filter(Calcao.forma_pagamento_id == filtro['formaPagamento'])

    if filtro['franquiado'] is not None:
        query = query.filter(Frota.fraqueado_id == filtro['franquiado'])

    if filtro.get('dataInicio') is not None:
        query = query.filter(Calcao.data_deposito >= filtro['dataInicio'])

    if filtro.get('dataFim') is not None:
        query = query.filter(Calcao.data_deposito <= filtro['dataFim'])

    return query

def filtros_basicos_semanais(query, filtro):
    if filtro.get('id') is not None:
        query = query.filter(Semanal.id == filtro['id'])

    if filtro['franquiado'] is not None:
        query = query.filter(Frota.fraqueado_id == filtro['franquiado'])

    if filtro.get('status') is not None:
        query = query.filter(Semanal.status_id == filtro['status'])

    if filtro.get('placa') is not None:
        query = query.filter(Semanal.frota_id == filtro['placa'])

    if filtro.get('dataInicio') is not None:
        query = query.filter(Semanal.data_prevista >= filtro['dataInicio'])

    if filtro.get('dataFim') is not None:
        query = query.filter(Semanal.data_prevista <= filtro['dataFim'])

    # query = query.filter(Semanal.deleted_at == None)

    return query

def filtros_basicos_custos_anuais(query, filtro):
    if filtro.get('id') is not None:
        query = query.filter(CustosAnuais.id == filtro['id'])

    if filtro.get('status') is not None:
        query = query.filter(CustosAnuais.status_id == filtro['status'])

    if filtro.get('frota') is not None:
        query = query.filter(CustosAnuais.frota_id == filtro['frota'])

    if filtro.get('dataInicio') is not None:
        query = query.filter(CustosAnuais.data_vencimento >= filtro['dataInicio'])

    if filtro.get('dataFim') is not None:
        query = query.filter(CustosAnuais.data_vencimento <= filtro['dataFim'])


    return query

def filtros_basicos_despesas(query, filtro):
    if filtro.get('id') is not None:
        query = query.filter(Despesa.id == filtro['id'])

    if filtro.get('mes') is not None:
        query = query.filter(Despesa.mes == filtro['mes'])

    if filtro.get('ano') is not None:
        query = query.filter(Despesa.ano == filtro['ano'])

    if filtro.get('dataInicio') is not None:
        query = query.filter(Despesa.updated_at >= filtro['dataInicio'])

    if filtro.get('dataFim') is not None:
        query = query.filter(Despesa.updated_at <= filtro['dataFim'])


    return query


def filtros_basicos_multas(query, filtro):
    if filtro.get('id') is not None:
        query = query.filter(Multa.id == filtro['id'])

    if filtro.get('status') is not None:
        query = query.filter(Multa.status_id == filtro['status'])

    if filtro.get('franqueado') is not None:
        query = query.filter(Frota.fraqueado_id == filtro['franqueado'])

    if filtro.get('frota') is not None:
        query = query.filter(Multa.frota_id == filtro['frota'])

    if filtro.get('formaPagamento') is not None:
        query = query.filter(Multa.forma_pagamento_id == filtro['formaPagamento'])

    if filtro.get('dataInicio') is not None:
        query = query.filter(Multa.data_infracao >= filtro['dataInicio'])

    if filtro.get('dataFim') is not None:
        query = query.filter(Multa.data_infracao <= filtro['dataFim'])

    if filtro.get('locatario') is not None:
        query = query.filter(Locatario.id == filtro['locatario'])

    return query

def filtros_basicos_faturamentos(query, filtro):
    if filtro.get('id') is not None:
        query = query.filter(Faturamento.id == filtro['id'])

    if filtro.get('status') is not None:
        query = query.filter(Faturamento.status_id == filtro['status'])

    if filtro.get('mes') is not None:
        query = query.filter(Faturamento.mes == filtro['mes'])

    if filtro.get('ano') is not None:
        query = query.filter(Faturamento.ano == filtro['ano'])

    if filtro.get('formaPagamento') is not None:
        query = query.filter(Faturamento.tipo_pagamento == filtro['formaPagamento'])

    if filtro.get('dataInicio') is not None:
        query = query.filter(Faturamento.data_pagamento >= filtro['dataInicio'])

    if filtro.get('dataFim') is not None:
        query = query.filter(Faturamento.data_pagamento <= filtro['dataFim'])

    return query


def filtros_basicos_oficina(query, filtro):
    if filtro.get('id') is not None:
        query = query.filter(Oficina.id == filtro['id'])

    if filtro.get('frota') is not None:
        query = query.filter(Oficina.frota_id == filtro['frota'])

    if filtro.get('dataInicio') is not None:
        query = query.filter(Oficina.data_servico >= filtro['dataInicio'])

    if filtro.get('dataFim') is not None:
        query = query.filter(Oficina.data_servico <= filtro['dataFim'])

    return query

def filtros_basicos_anexos(query, filtro):
    if filtro.get('id') is not None:
        query = query.filter(Anexo.id == filtro['id'])

    # if filtro['franquiado'] is not None:
    #     query = query.filter(Frota.fraqueado_id == filtro['franquiado'])

    # if filtro['locatario'] is not None:
    #     query = query.filter(Frota.fraqueado_id == filtro['locatario'])

    if filtro.get('tipo') is not None:
        query = query.filter(Anexo.entidade_tipo.like(f'{filtro['tipo']}%'))

    if filtro.get('codigo') is not None:
        query = query.filter(Anexo.entidade_id == filtro['codigo'])

    if filtro.get('extensao') is not None:
        query = query.filter(Anexo.tipo_mime.like(f'%{filtro['extensao']}%'))


    # query = query.filter(Semanal.deleted_at == None)

    return query