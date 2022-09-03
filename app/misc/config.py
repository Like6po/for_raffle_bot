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


@dataclass
class Redis:
    host: str
    port: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    redis: Redis
    timezone = timezone('Europe/Moscow')


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
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
    )


config = load_config("../.env")
