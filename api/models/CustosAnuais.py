from sqlalchemy import Column, Integer, String, Date, Numeric
from models.BaseModel import BaseModel

class CustosAnuais(BaseModel):
    __tablename__ = "custos_anuais"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    frota_id = Column(Integer, nullable=False)
    custo = Column(String(250), nullable=False)
    data_vencimento = Column(Date, nullable=False)
    parcela = Column(Integer, nullable=True)
    valor = Column(Numeric(10, 2), nullable=False)
    status_id = Column(Integer, nullable=False)
    log_id = Column(Integer, nullable=False)
