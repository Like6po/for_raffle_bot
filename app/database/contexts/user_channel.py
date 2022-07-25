import logging
from typing import Any, Union, Type

from aiogram.types.user import User as AiogramUser
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from database.contexts.base import DatabaseContext, SQLAlchemyModel
from database.models.user import User
from database.models.channel import Channel
from database.models.user_channel import UserChannel


class UserChannelContext(DatabaseContext):

    def __init__(
            self,
            session_or_pool: Union[sessionmaker, AsyncSession],
            *,
            query_model: Type[SQLAlchemyModel]):
        super().__init__(session_or_pool, query_model=query_model)

    async def get(self, user: User | None = None,
                  channel: Channel | None = None):
        if user and channel:
            return await super().get_one(UserChannel.user_id == user.id, UserChannel.channel_id == channel.id)
        elif user:
            return await super().get_all(UserChannel.user_id == user.id)
        elif channel:
            return await super().get_all(UserChannel.channel_id == channel.id)
        raise DataError

    async def new(self, user: User | None = None,
                  channel: Channel | None = None,
                  **values: Any) -> UserChannel:
        try:
            if user and channel:
                return await super().add(user_id=user.id,
                                         channel_id=channel.id,
                                         **values)
            raise DataError

        except IntegrityError as e:
            logging.exception("Не смог вставить в базу...", exc_info=e)

    async def check_and_create(self, user: User | None = None,
                               channel: Channel | None = None):
        if not await self.get(user, channel):
            return await self.new(user, channel)