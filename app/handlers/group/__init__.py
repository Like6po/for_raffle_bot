from aiogram import Router, Bot


def create_group_router(session_pool, bot: Bot) -> Router:
    r: Router = Router(name="group_router")

    return r
