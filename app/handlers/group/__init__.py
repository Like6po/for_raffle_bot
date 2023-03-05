from aiogram import Router
from aiogram.types import ContentType

from filters.chat_type import GroupChatFilter
from middlewares.leave_groups import LeaveGroupsMiddleware


async def group_leaver(*_):
    # фиктивный хендлер для работы мидлваря
    pass


def create_group_router() -> Router:
    group_router: Router = Router(name="group_router")

    group_router.message.bind_filter(bound_filter=GroupChatFilter)
    group_router.chat_member.bind_filter(bound_filter=GroupChatFilter)
    group_router.my_chat_member.bind_filter(bound_filter=GroupChatFilter)
    group_router.callback_query.bind_filter(bound_filter=GroupChatFilter)
    group_router.edited_message.bind_filter(bound_filter=GroupChatFilter)

    group_router.message.middleware(LeaveGroupsMiddleware())
    group_router.chat_member.middleware(LeaveGroupsMiddleware())
    group_router.my_chat_member.middleware(LeaveGroupsMiddleware())
    group_router.callback_query.middleware(LeaveGroupsMiddleware())
    group_router.edited_message.middleware(LeaveGroupsMiddleware())

    group_router.message.register(group_leaver, content_types=ContentType.ANY)
    group_router.callback_query.register(group_leaver)
    group_router.edited_message.register(group_leaver, content_types=ContentType.ANY)
    group_router.my_chat_member.register(group_leaver)
    group_router.chat_member.register(group_leaver)

    return group_router
