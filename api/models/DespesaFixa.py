from sqlalchemy import Column, Integer, String, Date, Numeric
from models.BaseModel import BaseModel

class DespesaFixa(BaseModel):
    __tablename__ = "despesas_fixas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    franquia_franquiador_locatario_id = Column(Integer, nullable=False)
    frota_id = Column(Integer, nullable=False)
    data = Column(Date, nullable=True)
    descricao = Column(String(100), nullable=False)
    valor = Column(Numeric(10, 2), nullable=True)
    log_id = Column(Integer, nullable=False)

