from sqlalchemy import Column, Integer

from database import DatabaseModel


class UserChannel(DatabaseModel):
    id = Column(Integer(), autoincrement=True, primary_key=True)
    user_id = Column(Integer(), nullable=False)
    channel_id = Column(Integer(), nullable=False)
