from fastapi import APIRouter, Depends, File, UploadFile, Request
from sqlalchemy.orm import Session
from controllers.SemanaisController import SemanaisController
from config.database import get_db
from config.dependencies import usuario_logado
from datetime import date
from fastapi.responses import Response

router = APIRouter()


@router.post("/create")
def create(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = SemanaisController(db)
    return controller.create_semanais(data, dados_token)

@router.put("/update/{semanal_id}")
def update(semanal_id: int, data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = SemanaisController(db)
    return controller.update_semanais(semanal_id, data, dados_token)

@router.delete("/delete/{semanal_id}")
def delete(semanal_id: int, dados_token = Depends(usuario_logado),db: Session = Depends(get_db)):
    controller = SemanaisController(db)
    return controller.delete_semanais(semanal_id, dados_token)

@router.get("/status/{semanal_id}")
def sfdelete(semanal_id: int, ativa: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = SemanaisController(db)
    return controller.sfdelete_semanais(semanal_id, ativa, dados_token)

@router.post("/automatico")
def automatico(data: dict, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = SemanaisController(db)
    return controller.gerar_semanais(data, dados_token)

@router.get("/listar")
def listar(
        dados_token = Depends(usuario_logado), 
        id: int = None,
        placa: int = None,
        status: int = None,
        franquiado: int = None,
        dataInicio: date = None, 
        dataFim: date = None,
        db: Session = Depends(get_db)
    ):
    filtros_url = {
        "id": id,
        "placa": placa,
        "status": status,
        "franquiado": franquiado,
        "dataInicio": dataInicio, 
        "dataFim": dataFim
    }
    controller = SemanaisController(db)
    return controller.listar_semanais(dados_token, filtros_url)

@router.post("/upload-imagem/{semanal_id}")
def upload_imagem_semanal(semanal_id: int, file: UploadFile = File(...), dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = SemanaisController(db)
    return controller.upload_imagem_semanal(semanal_id, file, dados_token)


@router.get("/imagem/{semanal_id}")
def get_imagem_semanal(
    semanal_id: int,
    db: Session = Depends(get_db)
):
    controller = SemanaisController(db)
    return controller.get_imagem_semanal(semanal_id)