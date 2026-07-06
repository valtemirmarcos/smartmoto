from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.FranquiadosController import FranquiadosController
from config.database import get_db
from config.dependencies import usuario_logado

router = APIRouter()


@router.post("/create")
def create(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FranquiadosController(db)
    return controller.create_franquiados(data)

@router.put("/update/{franquiado_id}")
def update(franquiado_id: int, data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FranquiadosController(db)
    return controller.update_franquiados(franquiado_id, data)

@router.delete("/delete/{franquiado_id}")
def delete(franquiado_id: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FranquiadosController(db)
    return controller.delete_franquiados(franquiado_id)

@router.get("/ativaDesativa/{franquiado_id}")
def sfdelete(franquiado_id: int, ativa: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FranquiadosController(db)
    return controller.sfdelete_franquiados(franquiado_id, ativa)

@router.get("/listar")
def listar(
    dados_token = Depends(usuario_logado), 
    id: int = None,
    ativa: int = None, 
    db: Session = Depends(get_db)
    ):
    filtros_url = {
        "id": id,
        "status": ativa
    }
    controller = FranquiadosController(db)
    return controller.listar_franquiados(dados_token, filtros_url)