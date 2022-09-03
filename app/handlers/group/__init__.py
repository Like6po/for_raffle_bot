from aiogram import Router


def create_group_router(*args) -> Router:
    r: Router = Router(name="group_router")

    return r
