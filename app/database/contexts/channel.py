import logging
from typing import Any, Union, Type

from aiogram.types.chat import Chat as AiogramChat
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from database.contexts.base import DatabaseContext, SQLAlchemyModel
from database.models.channel import Channel


class ChannelContext(DatabaseContext):

    def __init__(
            self,
            session_or_pool: Union[sessionmaker, AsyncSession],
            *,
            query_model: Type[SQLAlchemyModel]):
        super().__init__(session_or_pool, query_model=query_model)

    async def get(self, chat: AiogramChat | None = None,
                  tg_id: int | None = None):
        if chat:
            return await super().get_one(Channel.tg_id == chat.id)
        elif tg_id:
            return await super().get_one(Channel.tg_id == tg_id)
        raise DataError

    async def new(self, chat: AiogramChat | None = None,
                  tg_id: int | None = None,
                  username: str | None = None,
                  title: str | None = None,
                  **values: Any) -> Channel:
        try:
            if chat:
                return await super().add(tg_id=chat.id,
                                         title=chat.title,
                                         username=chat.username,
                                         **values)
            elif tg_id and title and username:
                return await super().add(tg_id=tg_id,
                                         title=title,
                                         username=username,
                                         **values)
            raise DataError

        except IntegrityError as e:
            logging.exception("Не смог вставить в базу...", exc_info=e)

    async def set(self,
                  chat: AiogramChat | None = None,
                  tg_id: int | None = None,
                  **values) -> None:
        if chat:
            return await super().update(Channel.tg_id == chat.id,
                                        title=chat.title,
                                        username=chat.username,
                                        **values)
        if tg_id:
            return await super().update(Channel.tg_id == tg_id, **values)

        raise DataError

    async def get_or_create_and_get(self, target_chat: AiogramChat | None = None):
        if data := await self.get(chat=target_chat):
            return data
        return await self.new(chat=target_chat)