from sqlalchemy import Column, Integer, String, Date, Numeric
from models.BaseModel import BaseModel

class Multa(BaseModel):
    __tablename__ = "multas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    franquia_franquiador_locatario_id = Column(Integer, nullable=False)
    frota_id = Column(Integer, nullable=False)
    codigo = Column(String(100), nullable=False)
    pontos = Column(Integer, nullable=True)
    data_infracao = Column(Date, nullable=False)
    data_notificacao = Column(Date, nullable=False)
    data_indicacao = Column(Date, nullable=False)
    data_pagamento = Column(Date, nullable=True)
    valor_multa = Column(Numeric(10, 2), nullable=False)
    valor_pago = Column(Numeric(10, 2), nullable=True)
    valor_recebido = Column(Numeric(10, 2), nullable=True)
    pagamento_id = Column(Integer, nullable=True)
    status_id = Column(Integer, nullable=False)
    log_id = Column(Integer, nullable=False)
    obs = Column(String(1000), nullable=True)

