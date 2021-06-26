from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, UniqueConstraint, func, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Connectivity(Base):
    __tablename__ = "connectivity"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    username1 = Column(String(length=50), nullable=False)
    username2 = Column(String(length=50), nullable=False)
    connected = Column(Boolean(), nullable=False)
    organisations = Column(JSON, server_default="[]")
    registered_at = Column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        Index('ix_connectivity_username1_username2', 'username1', 'username2'),
        # UniqueConstraint(
        #     'username1',
        #     'username2',
        #     name='uq_connectivity_username1_username2'
        # ),
    )
