from dataclasses import dataclass

from environs import Env
from pytz import timezone
from sqlalchemy.engine import URL


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int

    def construct_sqlalchemy_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            database=self.database,
            port=self.port
        )


@dataclass
class TgBot:
    token: str
    report_chat_id: int
    is_report_handler_error: bool


@dataclass
class Redis:
    host: str
    port: str


@dataclass
class Telegraph:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    redis: Redis
    telegraph: Telegraph
    timezone = timezone('Europe/Moscow')


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            report_chat_id=env.int("REPORT_CHAT_ID"),
            is_report_handler_error=env.bool("IS_REPORT_HANDLER_ERROR"),
        ),
        db=DbConfig(
            host=env.str('POSTGRES_HOST'),
            password=env.str('POSTGRES_PASSWORD'),
            user=env.str('POSTGRES_USER'),
            database=env.str('POSTGRES_DB'),
            port=env.int("POSTGRES_PORT")
        ),
        redis=Redis(
            host=env.str("REDIS_HOST"),
            port=env.str("REDIS_PORT")
        ),
        telegraph=Telegraph(
            token=env.str("TELEGRAPH_TOKEN")
        )
    )


config = load_config("../.env")
