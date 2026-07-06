from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.CodigosController import CodigosController
from config.database import get_db
from config.dependencies import usuario_logado

router = APIRouter()


@router.post("/create")
def create(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = CodigosController(db)
    return controller.create_codigos(data, dados_token)

@router.put("/update/{codigo_id}")
def update(codigo_id: int, data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = CodigosController(db)
    return controller.update_codigos(codigo_id, data, dados_token)

@router.delete("/delete/{codigo_id}")
def delete(codigo_id: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = CodigosController(db)
    return controller.delete_codigos(codigo_id, dados_token)

@router.get("/ativaDesativa/{codigo_id}")
def sfdelete(codigo_id: int, ativa: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = CodigosController(db)
    return controller.sfdelete_codigos(codigo_id, ativa, dados_token)