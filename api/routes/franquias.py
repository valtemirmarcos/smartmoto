from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.FranquiasController import FranquiasController
from config.database import get_db
from config.dependencies import usuario_logado

router = APIRouter()


@router.post("/create")
def create(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FranquiasController(db)
    return controller.create_franquias(data)

@router.put("/update/{franquia_id}")
def update(franquia_id: int, data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FranquiasController(db)
    return controller.update_franquias(franquia_id, data)

@router.delete("/delete/{franquia_id}")
def delete(franquia_id: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FranquiasController(db)
    return controller.delete_franquias(franquia_id)

@router.get("/ativaDesativa/{franquia_id}")
def sfdelete(franquia_id: int, ativa: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FranquiasController(db)
    return controller.sfdelete_franquias(franquia_id, ativa)