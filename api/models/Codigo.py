from sqlalchemy import Column, Integer, String
from models.BaseModel import BaseModel

class Codigo(BaseModel):
    __tablename__ = "codigos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    depara_id = Column(Integer, nullable=False)
    codigo = Column(Integer, nullable=False)
    descricao = Column(String(200), nullable=False)
    obs = Column(String(200), nullable=True)
    log_id = Column(Integer, nullable=False)