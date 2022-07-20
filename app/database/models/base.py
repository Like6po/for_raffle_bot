from __future__ import annotations

import logging
import re
from typing import Optional, Type, cast, Any, Dict, Pattern, Final

from sqlalchemy import inspect, Column, TIMESTAMP, func, Integer, Text, BigInteger, VARCHAR
from sqlalchemy.orm import registry, has_inherited_table, declared_attr
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.util import ImmutableProperties

mapper_registry = registry()

# Регулярное выражение, которое разделяет строку по заглавным буквам
TABLE_NAME_REGEX: Pattern[str] = re.compile(r"(?<=[A-Z])(?=[A-Z][a-z])|(?<=[^A-Z])(?=[A-Z])")
PLURAL: Final[str] = "s"

logger = logging.getLogger(__name__)


class DatabaseModel(metaclass=DeclarativeMeta):
    __abstract__ = True
    __mapper_args__ = {"eager_defaults": True}

    # noinspection PyUnusedLocal
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    registry = mapper_registry
    metadata = mapper_registry.metadata

    @declared_attr
    def __tablename__(self) -> Optional[str]:
        """
        Автоматически генерирует имя таблицы из названия модели, примеры:

        OrderItem -> order_items
        Order -> orders
        """
        if has_inherited_table(cast(Type[DatabaseModel], self)):
            return None
        cls_name = cast(Type[DatabaseModel], self).__qualname__
        table_name_parts = re.split(TABLE_NAME_REGEX, cls_name)
        formatted_table_name = "".join(
            table_name_part.lower() + "_" for i, table_name_part in enumerate(table_name_parts)
        )
        last_underscore = formatted_table_name.rfind("_")
        return formatted_table_name[:last_underscore] + PLURAL

    def _get_attributes(self) -> Dict[Any, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def __str__(self) -> str:
        attributes = "|".join(str(v) for k, v in self._get_attributes().items())
        return f"<{self.__class__.__qualname__} {attributes}>"

    def __repr__(self) -> str:
        table_attrs = cast(ImmutableProperties, inspect(self).attrs)
        primary_keys = " ".join(
            f"{key.name}={table_attrs[key.name].value}"
            for key in inspect(self.__class__).primary_key
        )
        return f"{self.__class__.__qualname__}->{primary_keys}"

    def as_dict(self) -> Dict[Any, Any]:
        return self._get_attributes()


class TimedBaseModel(DatabaseModel):
    __abstract__ = True
    id = Column(Integer(), autoincrement=True, primary_key=True)
    register_timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())
    # updated_at = Column(TIMESTAMP(timezone=True),
    #                     default=func.now(),
    #                     onupdate=func.now(),
    #                     server_default=func.now())


class User(DatabaseModel):
    id = Column(Integer(), autoincrement=True, primary_key=True)
    tg_id = Column(BigInteger(), unique=True, nullable=False)
    full_name = Column(VARCHAR(254), nullable=False)
