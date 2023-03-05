import logging
from typing import Any, Union, Type

from aiogram.types.user import User as AiogramUser
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from database.contexts.base import DatabaseContext, SQLAlchemyModel, ExpressionType
from database.models.user import User


class UserContext(DatabaseContext):
    def __init__(
            self,
            session_or_pool: Union[sessionmaker, AsyncSession],
            *,
            query_model: Type[SQLAlchemyModel]):
        super().__init__(session_or_pool, query_model=query_model)

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @user.deleter
    def user(self):
        del self._user

    async def get(self,
                  *clauses: ExpressionType,
                  user: AiogramUser | None = None,
                  tg_id: int | None = None,
                  username: str | None = None) -> User | None:
        if user:
            tg_id = user.id
            username = user.username
        if tg_id:
            return await super().get_one(User.tg_id == tg_id)
        if username:
            return await super().get_one(User.username == username)
        if clauses:
            return await super().get_one(*clauses)
        if self.user:
            return await super().get_one(User.tg_id == self.user.id)
        return None

    async def new(self, user: AiogramUser | None = None,
                  tg_id: int | None = None,
                  full_name: str | None = None,
                  username: str | None = None,
                  **values: Any) -> User:
        try:
            if user:
                return await super().add(tg_id=user.id,
                                         full_name=user.full_name,
                                         username=user.username,
                                         **values)
            if tg_id and full_name and username:
                return await super().add(tg_id=tg_id,
                                         full_name=full_name,
                                         username=username,
                                         **values)
            if self.user:
                return await super().add(tg_id=self.user.id,
                                         full_name=self.user.full_name,
                                         username=self.user.username,
                                         **values)
            else:
                return await super().add(**values)

        except IntegrityError as e:
            logging.exception("Не смог вставить в базу...", exc_info=e)

    async def set(self,
                  *clauses: ExpressionType,
                  user: AiogramUser | None = None,
                  tg_id: int | None = None,
                  **values) -> None:
        if user:
            return await super().update(User.tg_id == user.id,
                                        full_name=user.full_name,
                                        username=user.username,
                                        **values)
        if tg_id:
            return await super().update(User.tg_id == tg_id, **values)
        if clauses:
            return await super().update(*clauses, **values)
        if self.user:
            return await super().update(User.tg_id == self.user.id, **values)
        raise DataError

    async def get_or_create_and_get(self, target_user: AiogramUser | None = None):
        user = target_user if target_user is not None else self.user
        data = await self.get(user=user)
        if data:
            return data
        return await self.new(user=target_user)
