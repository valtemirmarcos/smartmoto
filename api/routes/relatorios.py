from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.RelatoriosController import RelatoriosController
from config.database import get_db
from config.dependencies import usuario_logado
from datetime import date

router = APIRouter()

@router.get("/dashboard")
def dashboard(
        dados_token = Depends(usuario_logado), 
        dataInicio: date = None, 
        dataFim: date = None,
        db: Session = Depends(get_db)
    ):
    filtros_url = {
        "dataInicio": dataInicio, 
        "dataFim": dataFim
    }
    controller = RelatoriosController(db)
    return controller.dashboard(dados_token, filtros_url)

@router.get("/custos")
def custos(
        dados_token = Depends(usuario_logado), 
        dataInicio: date = None, 
        dataFim: date = None,
        db: Session = Depends(get_db)
    ):
    filtros_url = {
        "dataInicio": dataInicio, 
        "dataFim": dataFim
    }
    controller = RelatoriosController(db)
    return controller.custos(dados_token, filtros_url)

@router.get("/custo_moto")
def custo_moto(
        dados_token = Depends(usuario_logado), 
        dataInicio: date = None, 
        dataFim: date = None,
        db: Session = Depends(get_db)
    ):
    filtros_url = {
        "dataInicio": dataInicio, 
        "dataFim": dataFim
    }
    controller = RelatoriosController(db)
    return controller.custo_moto(dados_token, filtros_url)

@router.get("/lucro_moto")
def lucro_moto(
        dados_token = Depends(usuario_logado), 
        dataInicio: date = None, 
        dataFim: date = None,
        db: Session = Depends(get_db)
    ):
    filtros_url = {
        "dataInicio": dataInicio, 
        "dataFim": dataFim
    }
    controller = RelatoriosController(db)
    return controller.lucro_moto(dados_token, filtros_url)