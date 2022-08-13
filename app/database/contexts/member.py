import logging
from typing import Any, Union, Type

from aiogram.types.user import User as AiogramUser
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from database.contexts.base import DatabaseContext, SQLAlchemyModel
from database.models.member import Member


class MemberContext(DatabaseContext):
    def __init__(
            self,
            session_or_pool: Union[sessionmaker, AsyncSession],
            *,
            query_model: Type[SQLAlchemyModel]):
        super().__init__(session_or_pool, query_model=query_model)

    async def get(self, user: AiogramUser | None = None,
                  tg_id: int | None = None,
                  db_id: int | None = None):
        if user:
            return await super().get_one(Member.tg_id == user.id)
        elif tg_id:
            return await super().get_one(Member.tg_id == tg_id)
        elif db_id:
            return await super().get_one(Member.id == db_id)
        raise DataError

    async def new(self, user: AiogramUser | None = None,
                  tg_id: int | None = None,
                  full_name: str | None = None,
                  username: str | None = None,
                  **values: Any) -> Member:
        try:
            if user:
                return await super().add(tg_id=user.id,
                                         full_name=user.full_name,
                                         username=user.username,
                                         **values)
            elif tg_id and full_name and username:
                return await super().add(tg_id=tg_id,
                                         full_name=full_name,
                                         username=username,
                                         **values)
            raise DataError

        except IntegrityError as e:
            logging.exception("Не смог вставить в базу...", exc_info=e)

    async def set(self, user: AiogramUser | None = None,
                  tg_id: int | None = None,
                  **values) -> None:
        if user:
            return await super().update(Member.tg_id == user.id,
                                        full_name=user.full_name,
                                        username=user.username,
                                        **values)
        if tg_id:
            return await super().update(Member.tg_id == tg_id, **values)

        raise DataError

    async def get_or_create_and_get(self, target_user: AiogramUser | None = None):
        if data := await self.get(user=target_user):
            return data
        return await self.new(user=target_user)
