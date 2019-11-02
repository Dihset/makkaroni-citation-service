from aiohttp import web
import aiohttp_cors

from .middlewares import error_middleware
from .routes import urls
from .settings import init_elasticsearch, close_elasticsearch


async def init_app():
    """App factory"""
    app = web.Application(
        middlewares=[
            error_middleware,
        ]
    )

    app.add_routes(urls)
    
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    
    for route in list(app.router.routes()):
        cors.add(route, webview=route.method == '*')

    app.on_startup.append(init_elasticsearch)
    app.on_cleanup.append(close_elasticsearch)

    return app
    