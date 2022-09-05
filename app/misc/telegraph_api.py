from aiograph import Telegraph

from misc.config import config


async def create_page_with_winners(content: str) -> str:
    telegraph = Telegraph(config.telegraph.token)
    page = await telegraph.create_page('🎉 Итоги Конкурса!', content=content)
    await telegraph.close()
    return page.url
