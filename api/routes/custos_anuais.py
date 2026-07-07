from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.CustosAnuaisController import CustosAnuaisController
from config.database import get_db
from config.dependencies import usuario_logado
from datetime import date

router = APIRouter()


@router.post("/create")
def create(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = CustosAnuaisController(db)
    return controller.create_custos_anuais(data, dados_token)

@router.put("/update/{custo_anual_id}")
def update(custo_anual_id: int, data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = CustosAnuaisController(db)
    return controller.update_custos_anuais(custo_anual_id, data, dados_token)

@router.delete("/delete/{custo_anual_id}")
def delete(custo_anual_id: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = CustosAnuaisController(db)
    return controller.delete_custos_anuais(custo_anual_id)

@router.get("/ativaDesativa/{custo_anual_id}")
def sfdelete(custo_anual_id: int, ativa: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = CustosAnuaisController(db)
    return controller.sfdelete_custos_anuais(custo_anual_id, ativa, dados_token)

@router.get("/listar")
def listar(
        dados_token = Depends(usuario_logado), 
        id: int = None,
        frota: int = None,
        status: int = None,
        dataInicio: date = None, 
        dataFim: date = None,
        db: Session = Depends(get_db)
    ):
    filtros_url = {
        "id": id,
        "frota": frota,
        "status": status,
        "dataInicio": dataInicio, 
        "dataFim": dataFim
    }
    controller = CustosAnuaisController(db)
    return controller.listar_custos_anuais(dados_token, filtros_url)