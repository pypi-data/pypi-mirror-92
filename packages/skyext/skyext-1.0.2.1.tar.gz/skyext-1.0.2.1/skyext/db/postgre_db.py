from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


class PG(object):
    def __init__(self):
        self._model = None
        self._session_factory = None
        self._session = None

    def init(self, url=None, **kwargs):
        if kwargs:
            self.engine = create_engine(url, **kwargs)
        else:
            self.engine = create_engine(url)

        self._session_factory = scoped_session(sessionmaker(bind=self.engine))
        self._model.metadata.create_all(self.engine)
        self._session = self._session_factory()

    @property
    def model(self):
        if not self._model:
            self._model = declarative_base()
        return self._model

    @property
    def session(self):
        if not self._session:
            self._session = self._session_factory()

        return self._session
