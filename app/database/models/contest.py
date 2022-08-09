from sqlalchemy import Column, Integer, BigInteger, VARCHAR, Text, Boolean, DateTime
from datetime import datetime

from database import DatabaseModel


class Contest(DatabaseModel):
    id = Column(Integer(), autoincrement=True, primary_key=True)
    channel_id = Column(Integer(), nullable=False)
    user_id = Column(Integer(), nullable=False)
    text = Column(Text(), nullable=False)
    btn_title = Column(Text(), nullable=False)
    attachment_hash = Column(Text())
    is_attachment_preview = Column(Boolean(), nullable=False)
    created_at = Column(DateTime(), nullable=False, default=datetime.now)
    start_at = Column(DateTime())
    end_at = Column(DateTime())
    end_count = Column(Integer())
    winner_count = Column(Integer(), nullable=False)
