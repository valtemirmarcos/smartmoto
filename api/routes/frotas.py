from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.FrotasController import FrotasController
from config.database import get_db
from config.dependencies import usuario_logado

router = APIRouter()


@router.post("/create")
def create(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FrotasController(db)
    return controller.create_frotas(data, dados_token)

@router.put("/update/{frota_id}")
def update(frota_id: int, data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FrotasController(db)
    return controller.update_frotas(frota_id, data, dados_token)

@router.delete("/delete/{frota_id}")
def delete(frota_id: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FrotasController(db)
    return controller.delete_frotas(frota_id, dados_token)

@router.get("/ativaDesativa/{frota_id}")
def sfdelete(frota_id: int, ativa: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = FrotasController(db)
    return controller.sfdelete_frotas(frota_id, ativa, dados_token)

@router.get("/listar")
def listar(
    dados_token = Depends(usuario_logado), 
    id: int = None, 
    status: int = None, 
    franquiado: int = None,
    placa: str = None,
    ano: int = None,
    cor: str = None,
    db: Session = Depends(get_db)):
    filtros_url = {
        "id": id,
        "status": status,
        "franquiado": franquiado,
        "placa":placa,
        "ano":ano,
        "cor": cor,
    }
    controller = FrotasController(db)
    return controller.listar_frotas(dados_token, filtros_url)
