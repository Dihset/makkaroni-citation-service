#!/usr/bin/env python
from aiohttp import web
from src import init_app


if __name__ == '__main__':
    web.run_app(init_app())
    