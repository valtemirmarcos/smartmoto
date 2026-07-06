from sqlalchemy import Column, Integer, String
from models.BaseModel import BaseModel

class Frota(BaseModel):
    __tablename__ = "frotas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    placa = Column(String(20), nullable=False)
    renavam = Column(String(30), nullable=False)
    ano = Column(Integer, nullable=False)
    modelo = Column(Integer, nullable=True)
    cor = Column(String(100), nullable=True)
    fraqueado_id = Column(Integer, nullable=False)
    status_id = Column(Integer, nullable=False)
    log_id = Column(Integer, nullable=False)
