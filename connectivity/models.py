from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Connectivity(Base):
    __tablename__ = "connectivity"

    id = Column(Integer, primary_key=True)
    user_handle1 = Column(String(length=100))
    user_handle2 = Column(String(length=100))
    is_connected = Column(Boolean())
    organisations = Column(JSON)
    registered_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            'user_handle1',
            'user_handle2',
            name='_user_handle_uc'
        ),
    )
