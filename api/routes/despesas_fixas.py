from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.DespesasFixasController import DespesasFixasController
from config.database import get_db
from config.dependencies import usuario_logado

router = APIRouter()


@router.post("/create")
def create(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = DespesasFixasController(db)
    return controller.create_despesas_fixas(data, dados_token)

@router.put("/update/{df_id}")
def update(df_id: int, data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = DespesasFixasController(db)
    return controller.update_despesas_fixas(df_id, data, dados_token)

@router.delete("/delete/{df_id}")
def delete(df_id: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = DespesasFixasController(db)
    return controller.delete_despesas_fixas(df_id, dados_token)

@router.get("/ativaDesativa/{df_id}")
def sfdelete(df_id: int, ativa: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = DespesasFixasController(db)
    return controller.sfdelete_despesas_fixas(df_id, ativa, dados_token)

@router.get("/listar")
def listar(
        dados_token = Depends(usuario_logado), 
        id: int = None,
        frota: int = None,
        db: Session = Depends(get_db)
    ):
    
    filtros_url = {
        "id": id,
        "frota": frota
    }

    controller = DespesasFixasController(db)

    return controller.listar_despesas_fixas(dados_token, filtros_url)