from sqlalchemy import Column, Integer, BigInteger, VARCHAR

from database.models import DatabaseModel


class User(DatabaseModel):
    id = Column(Integer(), autoincrement=True, primary_key=True)
    tg_id = Column(BigInteger(), unique=True, nullable=False)
    full_name = Column(VARCHAR(254), nullable=False)
    username = Column(VARCHAR(254), nullable=True, server_default=None)
