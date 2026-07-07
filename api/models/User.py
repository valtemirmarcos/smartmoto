from sqlalchemy import Column, Integer, String
from models.BaseModel import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    tipoAcessoID = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False, default=1)
    log_id = Column(Integer, nullable=False)


    # alembic revision --autogenerate -m "create users table"
    # alembic upgrade head