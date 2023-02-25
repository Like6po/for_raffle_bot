from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_bot_commands(bot: Bot):
    default_ru = [BotCommand(command="start", description="Главное меню.")]

    data = [
        (
            default_ru,
            BotCommandScopeDefault(),
            'ru'
        )
    ]

    for commands_list, commands_scope, language in data:
        await bot.set_my_commands(commands=commands_list, scope=commands_scope, language_code=language)
