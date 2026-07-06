from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import LONGTEXT

from models.BaseModel import BaseModel


class Anexo(BaseModel):
    __tablename__ = "anexos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    franquia_franquiador_locatario_id = Column(Integer, nullable=True)
    # semanal, multa, calcao
    entidade_tipo = Column(String(20), nullable=False)
    # id do registro na tabela correspondente
    entidade_id = Column(Integer, nullable=False)
    nome_arquivo = Column(String(255), nullable=True)
    tipo_mime = Column(String(100), nullable=True)
    log_id = Column(Integer, nullable=False)
    drive_file_id = Column(String(255), nullable=True)
    drive_link = Column(String(500), nullable=True)