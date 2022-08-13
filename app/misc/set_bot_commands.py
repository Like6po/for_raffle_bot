from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
# , BotCommandScopeAllChatAdministrators, BotCommandScopeAllPrivateChats


async def set_bot_commands(bot: Bot):
    default_ru = [BotCommand(command="start", description="Главное меню.")]

    # default_en = [BotCommand(command="stats", description="Send command usage statistics."),
    #               BotCommand(command="bb", description="Status of Boom Beach servers."),
    #               BotCommand(command="bs", description="Status of Brawl Stars servers."),
    #               BotCommand(command="cm", description="Status of Clash Mini servers."),
    #               BotCommand(command="coc", description="Status of Clash Of Clans servers."),
    #               BotCommand(command="cq", description="Status of Clash Quest servers."),
    #               BotCommand(command="cr", description="Status of Clash Royale servers."),
    #               BotCommand(command="e", description="Status of Everdale servers."),
    #               BotCommand(command="hd", description="Status of Hay Day servers.")]

    data = [
        (
            default_ru,
            BotCommandScopeDefault(),
            'ru'
        ),
        # (
        #     default_en,
        #     BotCommandScopeDefault(),
        #     'en'
        # ),
        # ADMIN COMMANDS #
        # (
        #     [BotCommand(command="settings", description="Настройки бота."),
        #      BotCommand(command="subscription", description="Настройки рассылки.")] + default_ru,
        #     BotCommandScopeAllChatAdministrators(),
        #     'ru'
        # ),
        # (
        #     [BotCommand(command="settings", description="Bot settings."),
        #      BotCommand(command="subscription", description="Subscription Settings.")] + default_en,
        #     BotCommandScopeAllChatAdministrators(),
        #     'en'
        # ),
        # PRIVATE CHAT COMMANDS #
        # (
        #     [BotCommand(command="settings", description="Настройки бота."),
        #      BotCommand(command="subscription", description="Настройки рассылки.")] + default_ru,
        #     BotCommandScopeAllPrivateChats(),
        #     'ru'
        # ),
        # (
        #     [BotCommand(command="settings", description="Bot settings."),
        #      BotCommand(command="subscription", description="Subscription Settings.")] + default_en,
        #     BotCommandScopeAllPrivateChats(),
        #     'en'
        # ),
    ]

    for commands_list, commands_scope, language in data:
        await bot.set_my_commands(commands=commands_list, scope=commands_scope, language_code=language)
