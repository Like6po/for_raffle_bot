from aiogram import Router
from aiogram.types import ContentType

from filters.chat_type import SuperGroupChatFilter
from middlewares.leave_groups import LeaveGroupsMiddleware


async def group_leaver(*_):
    # фиктивный хендлер для работы мидлваря
    pass


def create_super_group_router() -> Router:
    super_group_router: Router = Router(name="super_group_router")

    super_group_router.message.bind_filter(bound_filter=SuperGroupChatFilter)
    super_group_router.chat_member.bind_filter(bound_filter=SuperGroupChatFilter)
    super_group_router.my_chat_member.bind_filter(bound_filter=SuperGroupChatFilter)
    super_group_router.callback_query.bind_filter(bound_filter=SuperGroupChatFilter)
    super_group_router.edited_message.bind_filter(bound_filter=SuperGroupChatFilter)

    super_group_router.message.middleware(LeaveGroupsMiddleware())
    super_group_router.chat_member.middleware(LeaveGroupsMiddleware())
    super_group_router.my_chat_member.middleware(LeaveGroupsMiddleware())
    super_group_router.callback_query.middleware(LeaveGroupsMiddleware())
    super_group_router.edited_message.middleware(LeaveGroupsMiddleware())

    super_group_router.message.register(group_leaver, content_types=ContentType.ANY)
    super_group_router.callback_query.register(group_leaver)
    super_group_router.edited_message.register(group_leaver, content_types=ContentType.ANY)
    super_group_router.my_chat_member.register(group_leaver)
    super_group_router.chat_member.register(group_leaver)

    return super_group_router
