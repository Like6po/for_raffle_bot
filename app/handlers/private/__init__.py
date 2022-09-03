from aiogram import Router, F
from aiogram.dispatcher.filters.command import CommandStart
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from filters.chat_type import PrivateChatFilter
from handlers.private.addchannel.base import command_addchannel
from handlers.private.addchannel.callbacks.channels_add import channels_add
from handlers.private.addchannel.callbacks.channels_back import channels_back
from handlers.private.addchannel.callbacks.channels_cancel import channels_cancel
from handlers.private.addchannel.wait_channel import wait_channel
from handlers.private.contest.base import command_contest
from handlers.private.contest.callbacks.channel_choice import contest_channel_choice
from handlers.private.contest.callbacks.channel_switch import contest_channel_switch
from handlers.private.contest.callbacks.contest_close_contest import contest_close_cbq
from handlers.private.contest.callbacks.contest_condition import contest_condition
from handlers.private.contest.callbacks.contest_create import contest_create
from handlers.private.contest.callbacks.contest_results_change_page import contest_results_change_page_cbq
from handlers.private.contest.callbacks.contest_return import contest_return
from handlers.private.contest.callbacks.contest_show_result_button import choose_contest_to_finish_cbq
from handlers.private.contest.callbacks.post_preview import post_preview_cbq
from handlers.private.contest.collect_data import collect_data
from handlers.private.start.base import command_start
from handlers.private.start.callbacks.channels import start_channels
from handlers.private.start.callbacks.contest import start_contest
from handlers.private.start.deeplink import command_start_deeplink
from keyboards.channels import ChannelsCallback
from keyboards.contest import ContestCallback, JoinButtonCallback
from keyboards.results import ResultsCallback, ResultsChangePageCallback
from keyboards.start import StartCallback
from middlewares.init_contexts import InitMiddleware
from states.contest import ContestStatus
from states.user import UserStatus


def create_private_router(session_pool, bot_pickle, scheduler: AsyncIOScheduler) -> Router:
    private_router: Router = Router(name="private_router")

    private_router.message.bind_filter(bound_filter=PrivateChatFilter)
    private_router.callback_query.bind_filter(bound_filter=PrivateChatFilter)

    private_router.message.middleware(InitMiddleware(session_pool, bot_pickle, scheduler))
    private_router.callback_query.middleware(InitMiddleware(session_pool, bot_pickle, scheduler))

    private_router.message.register(command_start_deeplink, CommandStart(deep_link=True, deep_link_encoded=True))
    private_router.message.register(command_start, CommandStart())
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
    private_router.callback_query.register(choose_contest_to_finish_cbq, ContestCallback.filter(F.action == "results"))
    private_router.callback_query.register(post_preview_cbq, JoinButtonCallback.filter())
    private_router.callback_query.register(contest_close_cbq, ResultsCallback.filter())
    private_router.callback_query.register(contest_results_change_page_cbq, ResultsChangePageCallback.filter())

    return private_router
