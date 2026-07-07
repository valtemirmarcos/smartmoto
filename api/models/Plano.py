from sqlalchemy import Column, Integer, String, Numeric
from models.BaseModel import BaseModel

class Plano(BaseModel):
    __tablename__ = "planos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    plano = Column(String(100), nullable=False)
    descricao = Column(String(200), nullable=True)
    semanas = Column(Integer, nullable=False)
    valor = Column(Numeric(10, 2), nullable=True)
    log_id = Column(Integer, nullable=False)