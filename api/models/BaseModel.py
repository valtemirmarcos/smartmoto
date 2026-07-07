from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from config.database import Base


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
        default=None
    )