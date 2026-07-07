from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.LocatariosController import LocatariosController
from config.database import get_db
from config.dependencies import usuario_logado
from datetime import date

router = APIRouter()


@router.get("/listar")
def listar(dados_token = Depends(usuario_logado), id: int = None, placa: int = None, status: int = None, plano: int = None, nome: str = None, cpf: str = None, franquiado: int = None, dataInicio: date = None, dataFim: date = None,db: Session = Depends(get_db)):
    filtros_url = {
        "id": id,
        "status": status,
        "placa":placa,
        "plano": plano,
        "nome": nome,
        "cpf": cpf,
        "franquiado": franquiado,
        "dataInicio":dataInicio,
        "dataFim":dataFim,
    }
    controller = LocatariosController(db)
    return controller.listar_locatarios(dados_token, filtros_url)