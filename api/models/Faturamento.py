from sqlalchemy import Column, Integer, String, Date, Numeric
from models.BaseModel import BaseModel

class Faturamento(BaseModel):
    __tablename__ = "faturamentos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    franquia_franquiador_locatario_id = Column(Integer, nullable=False)
    frota_id = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    valor_entrada = Column(Numeric(10, 2), nullable=True)
    valor_saida = Column(Numeric(10, 2), nullable=True)
    data_pagamento = Column(Date, nullable=True)
    tipo_pagamento_id = Column(Integer, nullable=True)
    status_id = Column(Integer, nullable=False)
    log_id = Column(Integer, nullable=False)

