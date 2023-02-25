import logging
from datetime import datetime
from typing import Any, Union, Type, List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from sqlalchemy.orm import sessionmaker

from database.contexts.base import DatabaseContext, SQLAlchemyModel
from database.models.channel import Channel
from database.models.contest import Contest
from database.models.user import User


class ContestContext(DatabaseContext):
    def __init__(
            self,
            session_or_pool: Union[sessionmaker, AsyncSession],
            *,
            query_model: Type[SQLAlchemyModel]):
        super().__init__(session_or_pool, query_model=query_model)

    async def new(self, user: User | None = None,
                  channel: Channel | None = None,
                  text: str | None = None,
                  btn_title: str | None = None,
                  winner_count: int | None = None,
                  attachment_hash: str | None = None,
                  start_at: datetime | None = None,
                  end_at: datetime | None = None,
                  end_count: int | None = None,
                  channel_tg_id: int | None = None,
                  sponsor_channels: set | None = None,
                  is_notify_contest_end: bool = None,
                  **values: Any) -> Contest:
        try:
            if user and channel and text and winner_count and (end_at or end_count):
                return await super().add(user_id=user.id,
                                         channel_id=channel.id,
                                         channel_tg_id=channel_tg_id,
                                         text=text,
                                         btn_title=btn_title or "Учавствовать",
                                         attachment_hash=attachment_hash,
                                         start_at=start_at,
                                         end_at=end_at,
                                         end_count=end_count,
                                         winner_count=winner_count,
                                         sponsor_channels=sponsor_channels,
                                         is_notify_contest_end=is_notify_contest_end,
                                         **values)
            raise DataError

        except IntegrityError as e:
            logging.exception("Не смог вставить в базу...", exc_info=e)

    async def get_by_db_id(self, contest_db_id: int) -> Contest:
        return await super().get_one(Contest.id == contest_db_id)

    async def set_message_id(self, contest_db_id: int, message_id: int):
        await super().update(Contest.id == contest_db_id, message_id=message_id)

    async def get_all_active(self, channel_db_id: int) -> List[Contest]:
        return await super().get_all(Contest.channel_id == channel_db_id)

    async def get(self, channel_db_id: int,
                  limit=10,
                  offset=0) -> List[Contest]:
        statement = select(Contest).where(Contest.channel_id == channel_db_id).order_by(
            Contest.id.asc()).limit(limit=limit).offset(offset=offset)

        async with self._transaction:
            # noinspection PyTypeChecker
            result: AsyncResult = await self._session.execute(statement)
            first_scalar_result = result.scalars().all()
        return first_scalar_result  # type: ignore

    async def count(self, channel_db_id: int = None) -> int:
        return await super().count(Contest.channel_id == channel_db_id)

    async def finish(self, contest_db_id: int):
        return await super().delete(Contest.id == contest_db_id)
