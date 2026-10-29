from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.FaturamentosController import FaturamentosController
from config.database import get_db
from config.dependencies import usuario_logado
from datetime import date

router = APIRouter()


@router.post("/create")
def create(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FaturamentosController(db)
    return controller.create_faturamentos(data, dados_token)

@router.put("/update/{faturamento_id}")
def update(faturamento_id: int, data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FaturamentosController(db)
    return controller.update_faturamentos(faturamento_id, data, dados_token)

@router.delete("/delete/{faturamento_id}")
def delete(faturamento_id: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FaturamentosController(db)
    return controller.delete_faturamentos(faturamento_id)

@router.get("/ativaDesativa/{faturamento_id}")
def sfdelete(faturamento_id: int, ativa: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FaturamentosController(db)
    return controller.sfdelete_faturamentos(faturamento_id, ativa, dados_token)

@router.get("/gerarFatura/{franquiado_id}")
def gerarFatura(franquiado_id: int, mes: str, ano:str, royaties:float, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FaturamentosController(db)
    return controller.gerarFatura(franquiado_id, mes, ano, dados_token, royaties)

@router.get("/listar")
def listar(
        dados_token = Depends(usuario_logado), 
        id: int = None,
        mes: int = None,
        ano: int = None,
        status: int = None,
        formaPagamento: str = None,
        dataInicio: date = None, 
        dataFim: date = None,
        db: Session = Depends(get_db)
    ):
    filtros_url = {
        "id": id,
        "mes": mes,
        "ano": ano,
        "status": status,
        "formaPagamento":formaPagamento,
        "dataInicio": dataInicio, 
        "dataFim": dataFim
    }
    controller = FaturamentosController(db)
    return controller.listar_faturamentos(dados_token, filtros_url)