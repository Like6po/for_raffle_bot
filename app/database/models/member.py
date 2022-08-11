from sqlalchemy import Column, INTEGER, BigInteger, VARCHAR

from database import DatabaseModel


class Member(DatabaseModel):
    id = Column(INTEGER(), autoincrement=True, primary_key=True)
    contest_db_id = Column(INTEGER(), nullable=False)
    tg_id = Column(BigInteger(), unique=True, nullable=False)
    full_name = Column(VARCHAR(254), nullable=False)
    username = Column(VARCHAR(254), nullable=True, server_default=None)
