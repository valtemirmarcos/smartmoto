from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.DespesasController import DespesasController
from config.database import get_db
from config.dependencies import usuario_logado

router = APIRouter()


@router.post("/create")
def create(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = DespesasController(db)
    return controller.create_despesas(data)

@router.put("/update/{df_id}")
def update(df_id: int, data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = DespesasController(db)
    return controller.update_despesas(df_id, data)

@router.delete("/delete/{df_id}")
def delete(df_id: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = DespesasController(db)
    return controller.delete_despesas(df_id)

@router.get("/ativaDesativa/{df_id}")
def sfdelete(df_id: int, ativa: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = DespesasController(db)
    return controller.sfdelete_despesas(df_id, ativa)