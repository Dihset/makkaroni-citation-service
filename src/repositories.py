from abc import ABCMeta, abstractmethod
from aiohttp.web import HTTPNotFound
from .models import Citation
from aioelasticsearch import Elasticsearch
from .settings import ELASTIC_VALUES


class CitationSource(metaclass=ABCMeta):

    @abstractmethod
    async def get_all(self, page=0, limit=10): pass

    @abstractmethod
    async def get_by_id(self, pk): pass

    @abstractmethod
    async def get_by_keywords(self, keywords): pass

    @abstractmethod
    async def get_fuzzy_content(self, string): pass

    @abstractmethod
    async def create(self, obj: Citation): pass

    @abstractmethod
    async def delete(self, pk): pass


class CitationRepository:

    def __init__(self, source: CitationSource):
        self.source = source

    async def get_all(self, page=0, limit=10):
        return await self.source.get_all(page, limit)

    async def get_by_id(self, pk):
        return await self.source.get_by_id(pk)

    async def get_by_keywords(self, keywords): 
        return await self.source.get_by_keywords(keywords)
    
    async def get_fuzzy_content(self, string):
        return await self.source.get_fuzzy_content(string)


    async def create(self, obj: Citation):
        return await self.source.create(obj)

    async def delete(self, pk):
        return await self.source.delete(pk)


class CitationElasticSource(CitationSource):

    def __init__(self, elastic: Elasticsearch):
        self.elastic: Elasticsearch = elastic

    async def get_all(self, page=0, limit=10):
        result = await self.elastic.search(**ELASTIC_VALUES,
            body={
                "query" : {
                    "match_all" : {}
                }
            }
        )
        return [Citation(dict(_id=data['_id'], **data['_source'])) for data in result['hits']['hits']]

    async def get_by_id(self, pk):
        result = await self.elastic.get(**ELASTIC_VALUES, id=pk)
        citation = Citation(result['_source'])
        citation._id = result['_id']
        return citation

    async def get_by_keywords(self, keywords):
        body = {
            "query" : {
                "bool" : {
                    "must": [{"match": {"keywords": word}} for word in keywords]
                }
            }
        }
        result = await self.elastic.search(**ELASTIC_VALUES, body=body)
        return [Citation(dict(_id=data['_id'], **data['_source'])) for data in result['hits']['hits']]
    
    async def get_fuzzy_content(self, string):
        result = await self.elastic.search(**ELASTIC_VALUES,
            body={
                "query": {
                    "multi_match": {
                        "fields": [ 
                            "name",  "inn", "kpp", "postIndex", 
                            "town", "address", "bank", "all_string"
                        ],
                        "query": string,
                        "fuzziness": "AUTO"
                    }
                }
            }
        )
        return result
    async def create(self, obj: Citation):
        result = await self.elastic.index(**ELASTIC_VALUES, body=obj.to_primitive())
        obj._id = result['_id']
        return obj

    async def delete(self, pk):
        await self.elastic.delete(**ELASTIC_VALUES, id=pk)
