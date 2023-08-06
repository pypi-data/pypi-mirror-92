# -*- coding: utf8 -*-

from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch


class ElasticSearch(object):
    def __init__(self, hosts=None):
        self.conn = None
        if hosts:
            self.conn = Elasticsearch([hosts], max_retries=0)

    def init(self, config):
        if not config:
            return
        if not hasattr(config, "ELASTICSEARCH_HOST"):
            return
        if config.ELASTICSEARCH_HOST:
            self._init(hosts=config.ELASTICSEARCH_HOST)

    def _init(self, hosts=None, **kwargs):
        if hosts:
            self.conn = Elasticsearch([hosts], max_retries=0)

    def search(self, index, fields, mapping, **kwargs):
        res = Search(using=self.conn, index=index).source(fields)
        for key in kwargs.keys():
            res = res.filter("term", **{mapping[key]: kwargs[key]})
        res = res.scan()
        return [hit.to_dict() for hit in res]

    def index_exists(self, index):
        return self.conn.indices.exists(index=index)

    def add_index(self, index, body=None):
        self.conn.indices.create(index=index, ignore=400, body=body)

    def set_settings(self, index, settings):
        self.conn.indices.get_settings(
            index=index, doc_type=index, body=settings)

    def set_mapping(self, index, mapping):
        self.conn.indices.put_mapping(
            index=index, doc_type=index, body=mapping)

    def add_data(self, index, data):
        self.conn.index(index=index, doc_type=index, body=data)

    def del_index(self, index):
        self.conn.indices.delete(index=index)
