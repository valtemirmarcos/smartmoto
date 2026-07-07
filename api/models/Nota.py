from sqlalchemy import Column, Integer, String, Date, Numeric
from models.BaseModel import BaseModel

class Nota(BaseModel):
    __tablename__ = "notas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    franquiador_id = Column(Integer, nullable=False)
    frota_id = Column(Integer, nullable=False)
    valor_bruto_rateado = Column(Numeric(10, 2), nullable=True)
    valor_liquido_rateado = Column(Numeric(10, 2), nullable=True)
    log_id = Column(Integer, nullable=False)


