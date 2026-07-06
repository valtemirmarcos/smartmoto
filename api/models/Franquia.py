from sqlalchemy import Column, Integer, String, Date, Numeric
from models.BaseModel import BaseModel

class Franquia(BaseModel):
    __tablename__ = "franquias"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    franquia = Column(String(200), nullable=False)
    cnpj = Column(String(30), nullable=False, unique=True)
    status_id = Column(Integer, nullable=False)
    log_id = Column(Integer, nullable=False)

