from aiogram import Router, Bot, F

from filters.chat_type import PrivateChatFilter
from handlers.private.addchannel.base import command_addchannel
from handlers.private.addchannel.callbacks.channels_add import channels_add
from handlers.private.addchannel.callbacks.channels_back import channels_back
from handlers.private.addchannel.callbacks.channels_cancel import channels_cancel
from handlers.private.addchannel.wait_channel import wait_channel
from handlers.private.start.base import command_start
from handlers.private.start.callbacks.base import start_channels
from keyboards.channels import ChannelsCallback
from keyboards.start import StartCallback
from middlewares.init_contexts import InitMiddleware
from states.user import UserStatus


def create_private_router(session_pool, bot: Bot) -> Router:
    private_router: Router = Router(name="private_router")

    private_router.message.bind_filter(bound_filter=PrivateChatFilter)
    private_router.callback_query.bind_filter(bound_filter=PrivateChatFilter)

    private_router.message.middleware(InitMiddleware(session_pool, bot))
    private_router.callback_query.middleware(InitMiddleware(session_pool, bot))

    private_router.message.register(command_start, commands=["start"])
    private_router.message.register(command_addchannel, commands=["addchannel"], state=None)
    private_router.message.register(wait_channel, state=UserStatus.wait_channel_message)

    private_router.callback_query.register(start_channels, StartCallback.filter())
    private_router.callback_query.register(channels_back, ChannelsCallback.filter(F.action == "back"))
    private_router.callback_query.register(channels_add, ChannelsCallback.filter(F.action == "add"))
    private_router.callback_query.register(channels_cancel, ChannelsCallback.filter(F.action == "cancel"))

    return private_router
