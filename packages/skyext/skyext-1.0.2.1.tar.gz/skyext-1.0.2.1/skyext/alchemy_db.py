
__all__ = ['DB']

from sqlalchemy.ext.declarative import declarative_base

from skyext.db.postgre_db import PG

class DB(object):
    def __int__(self):
        self._url = None
        self._protocol = None
        self._model = None
        self._session = None
        self._db = None

    def init(self, config):
        if not config:
            return None
        if not hasattr(config, "SQLALCHEMY_DATABASE_URI"):
            return

        self._url = config.CACHE_URL
        url_protocol = str(self._url).lower().split(":")
        self._protocol = url_protocol[0]

        switch = {
            "postgresql+psycopg2": DBFactory.create_pg,
            "mysql": DBFactory.create_mysql
        }
        self._db = switch[self._protocol]()

    @property
    def model(self):
        if not self._model:
            if self._db:
                self._model = self._db.model
            else:
                self._model = declarative_base()

        return self._model

    @property
    def session(self):
        return self._db.session



class DBFactory(object):
    def __init__(self):
        pass

    @classmethod
    def create_pg(cls, url=None, **kwargs):
        if not url:
            return
        return PG().init(url=url, **kwargs)

    @classmethod
    def create_mysql(cls, config):
        pass
