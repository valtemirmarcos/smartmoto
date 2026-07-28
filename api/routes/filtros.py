from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.FiltrosController import FiltrosController
from config.database import get_db
from config.dependencies import usuario_logado

router = APIRouter()

# dados_token = Depends(usuario_logado)

@router.get("/frota/status")
def frota_status(db: Session = Depends(get_db)):
    controller = FiltrosController(db)
    return controller.frota_status()

@router.get("/locatario/status")
def locatario_status(db: Session = Depends(get_db)):
    controller = FiltrosController(db)
    return controller.locatario_status()

@router.get("/calcao/status")
def calcao_status(db: Session = Depends(get_db)):
    controller = FiltrosController(db)
    return controller.calcao_status()

@router.get("/semanais/status")
def semanais_status(db: Session = Depends(get_db)):
    controller = FiltrosController(db)
    return controller.semanais_status()

@router.get("/multas/status")
def multas_status(db: Session = Depends(get_db)):
    controller = FiltrosController(db)
    return controller.multas_status()

@router.get("/faturamentos/status")
def faturamentos_status(db: Session = Depends(get_db)):
    controller = FiltrosController(db)
    return controller.faturamentos_status()

@router.get("/faturamentos/tipos")
def faturamentos_tipos(db: Session = Depends(get_db)):
    controller = FiltrosController(db)
    return controller.faturamentos_tipos()

@router.get("/planos")
def filtro_planos(db: Session = Depends(get_db)):
    controller = FiltrosController(db)
    return controller.filtro_planos()

@router.get("/pagamentos")
def filtro_pagamentos(db: Session = Depends(get_db)):
    controller = FiltrosController(db)
    return controller.filtro_pagamentos()

@router.get("/custos/status")
def custos_status(db: Session = Depends(get_db)):
    controller = FiltrosController(db)
    return controller.custos_status()
