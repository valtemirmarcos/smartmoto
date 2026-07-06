from fastapi.responses import JSONResponse

import re
import os

from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone, date

import calendar

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def success_response(data=None, mensagem="Operação realizada com sucesso"):
    return {
        "status": "success",
        "data": {
            "mensagem": mensagem,
            "resultado": data
        }
    }


def exception_response(data=None, mensagem="Erro na operação", status_code=400):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "exception",
            "data": {
                "mensagem": mensagem,
                "resultado":data
            }
        }
    )

def apenasNumeros(campo):
    cnplimpo = re.sub(r"\D", "", campo)
    return cnplimpo

def remove_campos(data: dict, campos: list):
    for campo in campos:
        data.pop(campo, None)
    return data

def valida_placa(texto):
    # Normaliza (remove caracteres inválidos e deixa maiúsculo)
    placa = re.sub(r'[^A-Za-z0-9]', '', texto).upper()
    
    # Padrões
    padrao_antigo = r'^[A-Z]{3}[0-9]{4}$'      # ABC1234
    padrao_mercosul = r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$'  # ABC1D23
    
    if re.match(padrao_antigo, placa) or re.match(padrao_mercosul, placa):
        return placa  # retorna a placa válida normalizada
    
    raise ValueError(f"Placa inválida: {texto}")

def validar_campos_obrigatorios(campos_obrigatorios, dados):
    faltando = []
    
    for campo in campos_obrigatorios:
        if campo not in dados or dados[campo] in [None, ""]:
            faltando.append(campo)
    
    if faltando:
        raise ValueError(f"Campos obrigatórios ausentes ou inválidos: {', '.join(faltando)}")
    
    return True


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def ler_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        exp = payload.get("exp")

        # tempo atual em UTC (timestamp)
        now = datetime.now(timezone.utc).timestamp()

        # segundos restantes
        tempo_restante = int(exp - now)

        return {
            "valido": True,
            "expirado": False,
            "dados": payload,
            "expira_em_segundos": tempo_restante,
            "expira_em_minutos": round(tempo_restante / 60, 2)
        }

    except ExpiredSignatureError as e:
        # mesmo expirado, conseguimos ler o payload sem validar exp
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})

        exp = payload.get("exp")
        now = datetime.now(timezone.utc).timestamp()

        tempo_expirado = int(now - exp)

        return {
            "valido": False,
            "expirado": True,
            "dados": payload,
            "expirou_ha_segundos": tempo_expirado,
            "expirou_ha_minutos": round(tempo_expirado / 60, 2),
            "erro": "Token expirado"
        }

    except JWTError:
        return {
            "valido": False,
            "expirado": False,
            "dados": None,
            "erro": "Token inválido"
        }

def dia_semana_extenso(numero_dia):
    dias = [
        "Segunda",
        "Terça",
        "Quarta",
        "Quinta",
        "Sexta",
        "Sábado",
        "Domingo"
    ]

    return dias[numero_dia]

def datas_do_dia_semana_mes(numero_dia, ano=None, mes=None):

    hoje = date.today()

    if ano is None:
        ano = hoje.year

    if mes is None:
        mes = hoje.month

    _, ultimo_dia = calendar.monthrange(ano, mes)

    datas = []

    for dia in range(1, ultimo_dia + 1):
        data = date(ano, mes, dia)

        if data.weekday() == numero_dia:
            datas.append(data.strftime("%Y-%m-%d"))

    return datas

def calcular_data_pagamento(dia):
    hoje = date.today()

    # Se passou do dia 10, agenda para dia 10 do próximo mês
    if hoje.day > dia:
        if hoje.month == 12:
            ano = hoje.year + 1
            mes = 1
        else:
            ano = hoje.year
            mes = hoje.month + 1
    else:
        ano = hoje.year
        mes = hoje.month

    return date(ano, mes, dia)

def formatar_placa(placa: str) -> str:
    placa = placa.upper().replace(" ", "").replace("-", "")
    
    if len(placa) == 7:
        return f"{placa[:3]}-{placa[3:]}"  # ABC-1234 ou ABC-1D23
    
    return placa

def filtro_basico(modelo, dados: dict, campos: list = None) -> list:
    filtros = []
    for campo, valor in dados.items():
        if campos and campo not in campos:  # ignora se não estiver na lista
            continue
        if valor is not None:
            atributo = getattr(modelo, campo, None)
            if atributo is not None:
                filtros.append(atributo == valor)
    return filtros

def dataHora_formatada(data_str):
    data = datetime.fromisoformat(data_str)

    formatada = data.strftime("%d/%m/%Y %H:%M:%S")
    return formatada