from datetime import datetime

from sqlalchemy import Column, Integer, BigInteger, VARCHAR, DateTime, SmallInteger

from database import DatabaseModel


class Contest(DatabaseModel):
    id = Column(Integer(), autoincrement=True, primary_key=True)
    created_at = Column(DateTime(), nullable=False, default=datetime.now)
    channel_id = Column(BigInteger(), nullable=False)
    user_id = Column(BigInteger(), nullable=False)
    message_id = Column(BigInteger(), nullable=True)
    text = Column(VARCHAR(4096), nullable=False)
    btn_title = Column(VARCHAR(64), nullable=False)
    attachment_hash = Column(VARCHAR(256), nullable=True)
    start_at = Column(DateTime(), nullable=True)
    end_at = Column(DateTime(), nullable=True)
    end_count = Column(Integer(), nullable=True)
    winner_count = Column(SmallInteger(), nullable=False)
