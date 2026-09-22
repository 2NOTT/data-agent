from elasticsearch import AsyncElasticsearch


class ValueESRepository:
    def __init__(self,client:AsyncElasticsearch):
        self.client=client