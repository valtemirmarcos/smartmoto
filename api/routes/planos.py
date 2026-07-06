from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.PlanosController import PlanosController
from config.database import get_db
from config.dependencies import usuario_logado

router = APIRouter()


@router.post("/create")
def create(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = PlanosController(db)
    return controller.create_planos(data)

@router.put("/update/{plano_id}")
def update(plano_id: int, data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = PlanosController(db)
    return controller.update_planos(plano_id, data)

@router.delete("/delete/{plano_id}")
def delete(plano_id: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = PlanosController(db)
    return controller.delete_planos(plano_id)

@router.get("/ativaDesativa/{plano_id}")
def sfdelete(plano_id: int, ativa: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = PlanosController(db)
    return controller.sfdelete_planos(plano_id, ativa)