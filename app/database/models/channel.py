from sqlalchemy import Column, Integer, BigInteger, VARCHAR, Text

from database import DatabaseModel


class Channel(DatabaseModel):
    id = Column(Integer(), autoincrement=True, primary_key=True)
    tg_id = Column(BigInteger(), unique=True, nullable=False)Eke
    username = Column(VARCHAR(254), nullable=True, server_default=None)
    title = Column(Text(), nullable=False)