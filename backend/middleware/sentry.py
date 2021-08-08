from typing import List, OrderedDict, Optional
from ..schemas import RoomInfo
from fastapi import WebSocket
from starlette.types import ASGIApp, Receive, Scope, Send
from ..utils import after


class SentryMiddleware:
    def __init__(self, app: ASGIApp):
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        try:
            response = await self._app(scope, receive, send)
            return response
        except Exception as e:
            with sentry_sdk.push_scope() as scope:
                scope.set_context("request", request)
                scope.user = {
                    "ip_address": request.client.host,
                }
                sentry_sdk.capture_exception(e)
            raise e
