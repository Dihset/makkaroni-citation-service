import json

from aiohttp import web
from aiohttp.web import HTTPBadRequest, HTTPNotFound, json_response
from aiohttp_cors import CorsViewMixin
from .repositories import CitationRepository, CitationElasticSource
from .models import Citation


class CitationListView(web.View, CorsViewMixin):

    def __init__(self, request):
        super().__init__(request)
        self.repository = CitationRepository(
            CitationElasticSource(self.request.app['elastic'])
        )

    async def get(self):
        params = self.request.rel_url.query
        #page = int(params.get('page', 0))
        keywords = json.loads(params.get('keywords', '[]'))
        fuzzy = params.get('fuzzy', '')
        if keywords:
            resp = await self.repository.get_by_keywords(keywords)
        #elif fuzzy:
        #    resp = await self.repository.get_fuzzy_content(fuzzy)
        else:
            resp = await self.repository.get_all()
        return json_response([obj.to_primitive() for obj in resp])
    
    async def post(self):
        data = await self.request.json()
        obj = Citation(data)
        obj.validate()
        obj = await self.repository.create(obj)
        return json_response(obj.to_primitive(), status=201)


class CitationView(web.View, CorsViewMixin):
    
    def __init__(self, request):
        super().__init__(request)
        self._id = self.request.match_info['pk']
        self.repository = CitationRepository(
            CitationElasticSource(self.request.app['elastic'])
        )

    async def get(self):
        obj = await self.repository.get_by_id(self._id)
        return json_response(obj.to_primitive())
    
    async def put(self):
        pass
        #obj = await self._get_obj()
        #data = await self.request.json()
        #obj.import_data(data)
        #obj.updated_at = datetime.datetime.now()
        #await obj.save()
        #return json_response(obj.to_primitive())
    
    async def delete(self):
        obj = await self.repository.get_by_id(self._id)
        await self.repository.delete(self._id)
        return json_response(obj.to_primitive())


#async def fuzzy_search_view(request):
#    data = await request.json()
#    if 'fuzzy' not in data.keys():
#        raise HTTPBadRequest(text='fuzzy field is required')
#    repository = CitationRepository(
#        CitationElasticSource(request.app['elastic'])
#    )
#    return json_response(await repository.fuzzy_search(data['fuzzy']))
#
#
#async def search_by_inn(request):
#    inn = request.match_info['inn']
#    repository = CitationRepository(
#        CitationElasticSource(request.app['elastic'])
#    )
#    contractors = await repository.search_by_inn(inn)
#    return json_response([сontractor.to_primitive() for сontractor in contractors])
#
