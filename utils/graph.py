from datetime import date

from telegraph.aio import Telegraph


class Graph:

    def __init__(self, token: str):
        self.graph = Telegraph(token)

    async def create_page(self, alias: str, html_content: str):
        page = await self.graph.create_page(
            title=f'Правила от {date.today().isoformat()}',
            html_content=html_content,
            author_name='F3new',
            author_url='https://t.me/F3newtg'
        )
        return await self.to_tortoise_model(alias, page)


    async def edit_page(self, alias: str, path: str, html_content: str):
        page = await self.graph.edit_page(
            path=path,
            title=f'Правила от {date.today().isoformat()}',
            html_content=html_content,
            author_name='F3new',
            author_url='https://t.me/F3newtg'
        )
        return await self.to_tortoise_model(alias, page)

    async def get_auth_url(self) -> str:
        return (await self.graph.get_account_info(['auth_url']))['auth_url']

    @staticmethod
    async def to_tortoise_model(alias: str, page):
        from database.models import GraphPage
        return GraphPage(
            alias=alias,
            path=page['path'],
            url=page['url'],
            title=page['title'],
            author_name=page['author_name'],
            author_url=page['author_url']
        )
