from sqlalchemy import Column, Integer, String, Date, Numeric
from config.database import Base

class FranquiaFraqueadoLocatario(Base):
    __tablename__ = "franquias_fraqueados_locatarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    franquia_id = Column(Integer, nullable=False)
    franquiado_id = Column(Integer, nullable=True)
    locatarios_id = Column(Integer, nullable=True)
    log_id = Column(Integer, nullable=False)



