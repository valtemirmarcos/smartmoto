from sqlalchemy import Column, Integer, String, Date, Numeric
from models.BaseModel import BaseModel

class Calcao(BaseModel):
    __tablename__ = "calcoes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    franquia_franquiador_locatario_id = Column(Integer, nullable=False)
    frota_id = Column(Integer, nullable=False)
    data_deposito = Column(Date, nullable=True)
    forma_pagamento_id = Column(Integer, nullable=True)
    valor = Column(Numeric(10, 2), nullable=True)
    valor_atual = Column(Numeric(10, 2), nullable=True)
    status_id = Column(Integer, nullable=True)
    log_id = Column(Integer, nullable=False)
