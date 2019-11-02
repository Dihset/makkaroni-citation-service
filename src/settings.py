import logging
import os
import pathlib

from aioelasticsearch import Elasticsearch


#Default
PROJECT_DIR = pathlib.Path(__file__).parent.parent

#Logger
logging.basicConfig(level=logging.DEBUG)


#Elasticsearch
ELASTIC_HOST = os.getenv('ELASTIC_HOST', 'localhost')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))
ELASTIC_INDEX = os.getenv('ELASTIC_INDEX', 'citation-index')
ELASTIC_DOC_TYPE = os.getenv('ELASTIC_DOC_TYPE', 'citation')
ELASTIC_VALUES = {'index': ELASTIC_INDEX, 'doc_type': ELASTIC_DOC_TYPE}
async def init_elasticsearch(app):
    app['elastic'] = Elasticsearch(f'http://{ELASTIC_HOST}:{ELASTIC_PORT}')

async def close_elasticsearch(app):
    await app['elastic'].close()
