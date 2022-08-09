import logging
from typing import Union, Type, cast

from aiogram.types.user import User as AiogramUser
from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, AsyncResult
from sqlalchemy.orm import sessionmaker

from database.contexts.base import DatabaseContext, SQLAlchemyModel
from database.models.channel import Channel
from database.models.user import User
from database.models.user_channel import UserChannel


class UserChannelContext(DatabaseContext):

    def __init__(
            self,
            session_or_pool: Union[sessionmaker, AsyncSession],
            *,
            query_model: Type[SQLAlchemyModel]):
        super().__init__(session_or_pool, query_model=query_model)

    async def new(self, user_id: int, channel_id: int) -> UserChannel:
        try:
            return await super().add(user_id=user_id,
                                     channel_id=channel_id)
        except IntegrityError as e:
            logging.exception("Не смог вставить в базу...", exc_info=e)

    async def check_exists(self, user_id: int, channel_id: int):
        statement = exists(self.model).where(UserChannel.user_id == user_id,
                                             UserChannel.channel_id == channel_id).select()
        async with self._transaction:
            result: AsyncResult = await self._session.execute(statement)
            return cast(bool, result.scalar())

    async def get_all_user_channels(self, user: AiogramUser | None = None):
        statement = select(UserChannel.channel_id, Channel.title, Channel.tg_id, Channel.username, Channel.id). \
            join(Channel, Channel.id == UserChannel.channel_id). \
            join(User, User.id == UserChannel.user_id). \
            where(User.tg_id == user.id)
        async with self._transaction:
            result: AsyncResult = await self._session.execute(statement)
            return result.all()
