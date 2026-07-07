from sqlalchemy import Column, Integer, String, Date, Numeric
from models.BaseModel import BaseModel

class Despesa(BaseModel):
    __tablename__ = "despesas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    franquia_franquiador_locatario_id = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    despesa = Column(String(100), nullable=False)
    valor = Column(Numeric(10, 2), nullable=True)
    log_id = Column(Integer, nullable=False)

