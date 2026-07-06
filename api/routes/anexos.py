from fastapi import APIRouter, Depends, File, UploadFile, Request, Form
from typing import Optional
from sqlalchemy.orm import Session
from controllers.AnexosController import AnexosController
from config.database import get_db
from config.dependencies import usuario_logado
from datetime import date
from fastapi.responses import Response

router = APIRouter()


@router.post("/create")
def create(
    franquia_franquiador_locatario_id: Optional[int] = Form(None),
    entidade_tipo: str = Form(...),
    entidade_id: int = Form(...),
    file: UploadFile = File(...),
    dados_token = Depends(usuario_logado),
    db: Session = Depends(get_db)
):
    data = {
        "franquia_franquiador_locatario_id": franquia_franquiador_locatario_id,
        "entidade_tipo": entidade_tipo,
        "entidade_id": entidade_id,
        "file": file
    }
    controller = AnexosController(db)
    return controller.create_anexos(data, dados_token)

@router.post("/update/{anexo_id}")
def update(
    anexo_id: int, 
    franquia_franquiador_locatario_id: Optional[int] = Form(None),
    entidade_tipo: str = Form(...),
    entidade_id: int = Form(...),
    file: UploadFile = File(...),
    dados_token = Depends(usuario_logado),
    db: Session = Depends(get_db)
):
    data = {
        "franquia_franquiador_locatario_id": franquia_franquiador_locatario_id,
        "entidade_tipo": entidade_tipo,
        "entidade_id": entidade_id,
        "file": file
    }
    controller = AnexosController(db)
    return controller.update_anexos(anexo_id, data, dados_token)

@router.delete("/delete/{anexo_id}")
def delete(anexo_id: int, dados_token = Depends(usuario_logado),db: Session = Depends(get_db)):
    controller = AnexosController(db)
    return controller.delete_anexos(anexo_id, dados_token)

@router.get("/status/{anexo_id}")
def sfdelete(anexo_id: int, ativa: int, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = AnexosController(db)
    return controller.sfdelete_anexos(anexo_id, ativa, dados_token)

@router.get("/listar")
def listar(
        dados_token = Depends(usuario_logado), 
        id: int = None,
        franquia_franquiador_locatario_id: int = None,
        tipo: str = None,
        codigo: int = None,
        extensao: str = None, 
        db: Session = Depends(get_db)
    ):
    filtros_url = {
        "id": id,
        "franquia_franquiador_locatario_id": franquia_franquiador_locatario_id,
        "tipo": tipo,
        "codigo": codigo,
        "extensao": extensao
    }
    controller = AnexosController(db)
    return controller.listar_anexos(dados_token, filtros_url)

@router.get("/imagem/{tipo}/{codigo}")
def ler_imagem(
    tipo: str,
    codigo: int,
    db: Session = Depends(get_db)
):
    controller = AnexosController(db)
    return controller.ler_imagem(tipo, codigo)
