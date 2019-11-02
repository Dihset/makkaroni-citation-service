from aiohttp import web

from .views import CitationListView, CitationView


urls = [
    web.view('/api/citations', CitationListView),
    web.view('/api/citations/{pk}', CitationView),
]
