from sqlalchemy import Column, INTEGER

from database import DatabaseModel


class ContestMember(DatabaseModel):
    id = Column(INTEGER(), autoincrement=True, primary_key=True)
    member_db_id = Column(INTEGER(), nullable=False)
    contest_db_id = Column(INTEGER(), nullable=False)
