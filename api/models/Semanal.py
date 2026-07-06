from sqlalchemy import Column, Integer, String, Date, Numeric, Text
from models.BaseModel import BaseModel
from sqlalchemy.dialects.mysql import LONGTEXT

class Semanal(BaseModel):
    __tablename__ = "semanais"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    franquia_franquiador_locatario_id = Column(Integer, nullable=False)
    frota_id = Column(Integer, nullable=False)
    data_prevista = Column(Date, nullable=True)
    valor = Column(Numeric(10, 2), nullable=True)
    data_pagamento = Column(Date, nullable=True)
    valor_pago = Column(Numeric(10, 2), nullable=True)
    status_id = Column(Integer, nullable=True)
    log_id = Column(Integer, nullable=False)
