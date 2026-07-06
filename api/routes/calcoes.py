from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.CalcoesController import CalcoesController
from config.database import get_db
from config.dependencies import usuario_logado
from datetime import date

router = APIRouter()


@router.post("/create")
def create(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = CalcoesController(db)
    return controller.create_calcoes(data, dados_token)

@router.put("/update/{calcao_id}")
def update(calcao_id: int, data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = CalcoesController(db)
    return controller.update_calcoes(calcao_id, data, dados_token)

@router.delete("/delete/{calcao_id}")
def delete(calcao_id: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = CalcoesController(db)
    return controller.delete_calcoes(calcao_id)

@router.get("/ativaDesativa/{calcao_id}")
def sfdelete(calcao_id: int, ativa: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = CalcoesController(db)
    return controller.sfdelete_calcoes(calcao_id, ativa, dados_token)

@router.get("/listar")
def listar(
        dados_token = Depends(usuario_logado), 
        id: int = None,
        placa: int = None,
        status: int = None,
        franquiado: int = None,
        formaPagamento: int = None,
        dataInicio: date = None, 
        dataFim: date = None,
        db: Session = Depends(get_db)
    ):
    filtros_url = {
        "id": id,
        "placa": placa,
        "status": status,
        "formaPagamento":formaPagamento,
        "franquiado": franquiado,
        "dataInicio": dataInicio, 
        "dataFim": dataFim
    }
    controller = CalcoesController(db)
    return controller.listar_calcoes(dados_token, filtros_url)