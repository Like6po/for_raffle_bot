from sqlalchemy import Column, INTEGER, BIGINT, VARCHAR

from database.models import DatabaseModel


class Member(DatabaseModel):
    id = Column(INTEGER(), autoincrement=True, primary_key=True)
    tg_id = Column(BIGINT(), unique=True, nullable=False)
    full_name = Column(VARCHAR(254), nullable=False)
    username = Column(VARCHAR(254), nullable=True, server_default=None)
