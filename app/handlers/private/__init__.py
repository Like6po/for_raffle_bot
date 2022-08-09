from aiogram import Router, Bot, F

from filters.chat_type import PrivateChatFilter
from handlers.private.addchannel.base import command_addchannel
from handlers.private.addchannel.callbacks.channels_add import channels_add
from handlers.private.addchannel.callbacks.channels_back import channels_back
from handlers.private.addchannel.callbacks.channels_cancel import channels_cancel
from handlers.private.addchannel.wait_channel import wait_channel
from handlers.private.start.base import command_start
from handlers.private.start.callbacks.channels import start_channels
from handlers.private.start.callbacks.contest import start_contest
from handlers.private.contest.base import command_contest
from handlers.private.contest.callbacks.channel_choice import contest_channel_choice
from handlers.private.contest.callbacks.channel_switch import contest_channel_switch
from handlers.private.contest.callbacks.contest_create import contest_create
from handlers.private.contest.callbacks.contest_return import contest_return
from handlers.private.contest.callbacks.contest_condition import contest_condition
from handlers.private.contest.collect_data import collect_data
from keyboards.channels import ChannelsCallback
from keyboards.start import StartCallback
from keyboards.contest import ContestCallback
from middlewares.init_contexts import InitMiddleware
from states.user import UserStatus
from states.contest import ContestStatus


def create_private_router(session_pool, bot: Bot) -> Router:
    private_router: Router = Router(name="private_router")

    private_router.message.bind_filter(bound_filter=PrivateChatFilter)
    private_router.callback_query.bind_filter(bound_filter=PrivateChatFilter)

    private_router.message.middleware(InitMiddleware(session_pool, bot))
    private_router.callback_query.middleware(InitMiddleware(session_pool, bot))

    private_router.message.register(command_start, commands=["start"])
    private_router.message.register(command_addchannel, commands=["addchannel"], state=None)
    private_router.message.register(command_contest, commands=["contest"])
    private_router.message.register(wait_channel, state=UserStatus.wait_channel_message)
    private_router.message.register(collect_data, state=ContestStatus)

    private_router.callback_query.register(start_channels, StartCallback.filter(F.action == "channels"))
    private_router.callback_query.register(channels_back, ChannelsCallback.filter(F.action == "back"))
    private_router.callback_query.register(channels_add, ChannelsCallback.filter(F.action == "add"))
    private_router.callback_query.register(channels_cancel, ChannelsCallback.filter(F.action == "cancel"))
    private_router.callback_query.register(start_contest, StartCallback.filter(F.action == "contest"))
    private_router.callback_query.register(contest_channel_choice, ContestCallback.filter(F.action == "channel_choice"))
    private_router.callback_query.register(contest_channel_switch, ContestCallback.filter(F.action == "channel_switch"))
    private_router.callback_query.register(contest_create, ContestCallback.filter(F.action == "create"))
    private_router.callback_query.register(contest_return, ContestCallback.filter(F.action == "return"))
    private_router.callback_query.register(contest_condition, ContestCallback.filter(F.action == "condition"))

    return private_router
