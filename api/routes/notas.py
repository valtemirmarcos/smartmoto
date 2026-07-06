from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.NotasController import NotasController
from config.database import get_db
from config.dependencies import usuario_logado

router = APIRouter()


@router.post("/create")
def create(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = NotasController(db)
    return controller.create_notas(data)

@router.put("/update/{nota_id}")
def update(nota_id: int, data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = NotasController(db)
    return controller.update_notas(nota_id, data)

@router.delete("/delete/{nota_id}")
def delete(nota_id: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = NotasController(db)
    return controller.delete_notas(nota_id)

@router.get("/ativaDesativa/{nota_id}")
def sfdelete(nota_id: int, ativa: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = NotasController(db)
    return controller.sfdelete_notas(nota_id, ativa)