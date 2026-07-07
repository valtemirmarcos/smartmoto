from sqlalchemy import Column, Integer, String, Date, Numeric
from models.BaseModel import BaseModel

class Locatario(BaseModel):
    __tablename__ = "locatarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    cpf = Column(String(30), nullable=True, unique=True)
    cnh = Column(String(50), nullable=True)
    endereco = Column(String(200), nullable=True)
    numero = Column(String(10), nullable=True)
    complemento = Column(String(100), nullable=True)
    cep = Column(String(15), nullable=True)
    cidade = Column(String(50), nullable=True)
    uf = Column(String(3), nullable=True)
    status_id = Column(Integer, nullable=False)
    frota_id = Column(Integer, nullable=False)
    plano_id = Column(Integer, nullable=True)
    data_inicio_contrato = Column(Date, nullable=True)
    log_id = Column(Integer, nullable=False)

