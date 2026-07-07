from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.OficinaController import OficinaController
from config.database import get_db
from config.dependencies import usuario_logado
from datetime import date

router = APIRouter()


@router.post("/create")
def create(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = OficinaController(db)
    return controller.create_oficina(data, dados_token)

@router.put("/update/{oficina_id}")
def update(oficina_id: int,  data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = OficinaController(db)
    return controller.update_oficina(oficina_id, data, dados_token)

@router.delete("/delete/{oficina_id}")
def delete(oficina_id: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = OficinaController(db)
    return controller.delete_oficina(oficina_id)

@router.get("/ativaDesativa/{oficina_id}")
def sfdelete(oficina_id: int, ativa: int,  dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = OficinaController(db)
    return controller.sfdelete_oficina(oficina_id, ativa, dados_token)

@router.get("/listar")
def listar(
        dados_token = Depends(usuario_logado), 
        id: int = None,
        frota: int = None,
        dataInicio: date = None, 
        dataFim: date = None,
        db: Session = Depends(get_db)
    ):
    filtros_url = {
        "id": id,
        "frota": frota,
        "dataInicio": dataInicio, 
        "dataFim": dataFim
    }
    controller = OficinaController(db)
    return controller.listar_oficina(dados_token, filtros_url)