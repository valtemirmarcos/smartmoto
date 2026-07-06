from fastapi import APIRouter
from controllers.BasicController import BasicController

router = APIRouter()
basicController = BasicController()

@router.get("/")
def helloa():
    return basicController.helloa()

@router.get("/hello")
def hello():
    return basicController.hello()

@router.get("/db-info")
def db_info():
    return basicController.db_info()