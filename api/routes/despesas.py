from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.DespesasController import DespesasController
from config.database import get_db
from config.dependencies import usuario_logado
from datetime import date

router = APIRouter()


@router.post("/create")
def create(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = DespesasController(db)
    return controller.create_despesas(data, dados_token)

@router.put("/update/{despesa_id}")
def update(despesa_id: int, data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = DespesasController(db)
    return controller.update_despesas(despesa_id, data, dados_token)

@router.delete("/delete/{despesa_id}")
def delete(despesa_id: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = DespesasController(db)
    return controller.delete_despesas(despesa_id)

@router.get("/ativaDesativa/{despesa_id}")
def sfdelete(despesa_id: int, ativa: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = DespesasController(db)
    return controller.sfdelete_despesas(despesa_id, ativa, dados_token)

@router.get("/listar")
def listar(
        dados_token = Depends(usuario_logado), 
        id: int = None,
        mes: int = None,
        ano: int = None,
        dataInicio: date = None, 
        dataFim: date = None,
        db: Session = Depends(get_db)
    ):
    filtros_url = {
        "id": id,
        "mes": mes,
        "ano": ano,
        "dataInicio": dataInicio, 
        "dataFim": dataFim
    }
    controller = DespesasController(db)
    return controller.listar_despesas(dados_token, filtros_url)