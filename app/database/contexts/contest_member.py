from typing import Union, Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from database.contexts.base import DatabaseContext, SQLAlchemyModel
from database import ContestMember


class ContestMemberContext(DatabaseContext):
    def __init__(
            self,
            session_or_pool: Union[sessionmaker, AsyncSession],
            *,
            query_model: Type[SQLAlchemyModel]):
        super().__init__(session_or_pool, query_model=query_model)

    async def add(self, contest_db_id: int,
                  member_db_id: int) -> ContestMember:
        return await super().add(contest_db_id=contest_db_id,
                                 member_db_id=member_db_id)

    async def exists(self, contest_db_id: int,
                     member_db_id: int) -> bool:
        return await super().exists(ContestMember.contest_db_id == contest_db_id,
                                    ContestMember.member_db_id == member_db_id)

    async def delete(self, contest_db_id: int,
                     member_db_id: int):
        return await super().delete(ContestMember.contest_db_id == contest_db_id,
                                    ContestMember.member_db_id == member_db_id)

    async def count(self, contest_db_id: int) -> int:
        return await super().count(ContestMember.contest_db_id == contest_db_id)
