from starlette.types import ASGIApp, Receive, Scope, Send
from .empathymansion import EmpathyMansion


class EmpathyEventMiddleware:
    def __init__(self, app: ASGIApp):
        self._app = app
        self._empathy_mansion = EmpathyMansion()

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] in ("lifespan", "http", "websocket"):
            scope["empathy_mansion"] = self._empathy_mansion
        await self._app(scope, receive, send)
