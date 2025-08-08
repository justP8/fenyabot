from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update


class AccessMiddleware(BaseMiddleware):
    """
    Middleware that only lets the admins in
    """
    def __init__(self, admins: list[str]) -> None:
        self.admins = list(map(int, admins))

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Callable[[Update, Dict[str, Any]], Awaitable[Any]] | None:
        print(data)
        if data['event_chat'].type == 'private' and data['event_from_user'].id not in self.admins:
            return
        return await handler(event, data)

