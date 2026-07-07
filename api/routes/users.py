from fastapi import APIRouter, Depends, Query, Request
from typing import Optional
from sqlalchemy.orm import Session
from controllers.UsersController import UsersController
from config.database import get_db
from config.dependencies import usuario_logado

router = APIRouter()

@router.get("/")
def helloa(db: Session = Depends(get_db)):
    controller = UsersController(db)
    return controller.helloa()

@router.get("/hello")
def hello(db: Session = Depends(get_db)):
    controller = UsersController(db)
    return controller.hello()

@router.get("/db-info")
def db_info(db: Session = Depends(get_db)):
    controller = UsersController(db)
    return controller.db_info()

@router.post("/create")
def create(data: dict, request: Request, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = UsersController(db)
    return controller.create_user(data, request, dados_token)

@router.put("/update/{user_id}")
def update_user(data: dict, user_id: int, request: Request, dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = UsersController(db)
    return controller.update_user(data, user_id, request, dados_token)

@router.get("/ativaDesativa/{user_id}")
def sfdelete(user_id: int, request: Request, ativa: Optional[int] = Query(None), dados_token = Depends(usuario_logado), db: Session = Depends(get_db)):
    controller = UsersController(db)
    return controller.sfdelete_users(user_id, ativa, request, dados_token)

@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    controller = UsersController(db)
    return controller.login(data)