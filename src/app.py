from aiohttp import web

from .middlewares import error_middleware
from .routes import urls


async def init_app():
    """App factory"""
    app = web.Application(
        middlewares=[
            error_middleware,
        ]
    )
    app.add_routes(urls)
    return app
    