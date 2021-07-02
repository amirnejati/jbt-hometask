from sqlalchemy import (
    JSON, Column, Integer, String, Index,
    # DateTime, Boolean, func
)

from db import Base


class Connectivity(Base):
    __tablename__ = "connectivity"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    username1 = Column(String(length=50), nullable=False)
    username2 = Column(String(length=50), nullable=False)
    invocation = Column(JSON, server_default="{}")

    __table_args__ = (
        Index('ix_connectivity_username1_username2', 'username1', 'username2'),
    )


# class Connectivity(Base):
#     __tablename__ = "connectivity"
#
#     id = Column(Integer, primary_key=True, autoincrement="auto")
#     username1 = Column(String(length=50), nullable=False)
#     username2 = Column(String(length=50), nullable=False)
#     connected = Column(Boolean(), nullable=False)
#     organisations = Column(JSON, server_default="[]")
#     registered_at = Column(DateTime, server_default=func.now(), nullable=False)
#
#     __table_args__ = (
#         Index('ix_connectivity_username1_username2', 'username1', 'username2'),
#         # sqlalchemy.UniqueConstraint(
#         #     'username1',
#         #     'username2',
#         #     name='uq_connectivity_username1_username2'
#         # ),
#     )
