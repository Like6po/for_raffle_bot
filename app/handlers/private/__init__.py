from aiogram import Router, Bot, F

from filters.chat_type import PrivateChatFilter
from middlewares.init_contexts import InitMiddleware
from .start.base import command_start
from .start_callback.base import start_channels
from .start_callback.channels import channels_back, channels_add
from .addchannel.base import command_addchannel
from .addchannel.state import state_addchannel

from states.user import UserStatus


def create_private_router(session_pool, bot: Bot) -> Router:
    private_router: Router = Router(name="private_router")

    # Сообщения
    private_router.message.bind_filter(bound_filter=PrivateChatFilter)
    private_router.message.middleware(InitMiddleware(session_pool, bot))
    private_router.callback_query.bind_filter(bound_filter=PrivateChatFilter)
    private_router.callback_query.middleware(InitMiddleware(session_pool, bot))

    private_router.message.register(command_start,
                                    commands=["start"])
    private_router.message.register(command_addchannel,
                                    commands=["addchannel"], state=None)

    private_router.message.register(state_addchannel, state=UserStatus.wait_channel_message)

    private_router.callback_query.register(start_channels, F.data == 'start:channels')
    private_router.callback_query.register(channels_back, F.data == 'channels:back')
    private_router.callback_query.register(channels_add, F.data == 'channels:add')

    return private_router
