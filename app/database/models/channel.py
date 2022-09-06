from sqlalchemy import Column, Integer, BigInteger, VARCHAR

from database.models import DatabaseModel


class Channel(DatabaseModel):
    id = Column(Integer(), autoincrement=True, primary_key=True)
    tg_id = Column(BigInteger(), unique=True, nullable=False)
    username = Column(VARCHAR(254), nullable=True, server_default=None)
    title = Column(VARCHAR(32), nullable=False)
