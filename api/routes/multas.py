from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.MultasController import MultasController
from config.database import get_db
from config.dependencies import usuario_logado
from datetime import date

router = APIRouter()


@router.post("/create")
def create(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = MultasController(db)
    return controller.create_multas(data, dados_token)

@router.put("/update/{multa_id}")
def update(multa_id: int, data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = MultasController(db)
    return controller.update_multas(multa_id, data, dados_token)

@router.delete("/delete/{multa_id}")
def delete(multa_id: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = MultasController(db)
    return controller.delete_multas(multa_id)

@router.get("/ativaDesativa/{multa_id}")
def sfdelete(multa_id: int, ativa: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = MultasController(db)
    return controller.sfdelete_multas(multa_id, ativa, dados_token)

@router.get("/listar")
def listar(
        dados_token = Depends(usuario_logado), 
        id: int = None,
        franqueado: int = None,
        frota: int = None,
        status: int = None,
        formaPagamento: int = None,
        dataInicio: date = None, 
        dataFim: date = None,
        locatario: int = None,
        db: Session = Depends(get_db)
    ):
    filtros_url = {
        "id": id,
        "franqueado": franqueado,
        "frota": frota,
        "status": status,
        "formaPagamento":formaPagamento,
        "dataInicio": dataInicio, 
        "dataFim": dataFim,
        "locatario": locatario
    }
    controller = MultasController(db)
    return controller.listar_multas(dados_token, filtros_url)