from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.CobrancasController import CobrancasController
from config.database import get_db
from config.dependencies import usuario_logado

router = APIRouter()


@router.post("/create")
def create(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = CobrancasController(db)
    return controller.create_cobrancas(data)

@router.put("/update/{cobranca_id}")
def update(cobranca_id: int, data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = CobrancasController(db)
    return controller.update_cobrancas(cobranca_id, data)

@router.delete("/delete/{cobranca_id}")
def delete(cobranca_id: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = CobrancasController(db)
    return controller.delete_cobrancas(cobranca_id)

@router.get("/ativaDesativa/{cobranca_id}")
def sfdelete(cobranca_id: int, ativa: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = CobrancasController(db)
    return controller.sfdelete_cobrancas(cobranca_id, ativa)