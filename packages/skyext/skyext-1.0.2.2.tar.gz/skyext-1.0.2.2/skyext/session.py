from skyext.db.redis_db import Redis

__all__ = ('Session',)


class Session(object):
    def __int__(self):
        self._url = None
        self._protocol = None
        self._client = None

    def init(self, config):
        if not config:
            return None
        if not hasattr(config, "SESSION_URL"):
            return

        self._url = config.CACHE_URL
        url_protocol = str(self._url).lower().split(":")
        self._protocol = url_protocol

        switch = {
            "redis": SessionFactory.create_redis,
            "membercache": SessionFactory.create_member,
            "file": SessionFactory.create_file,
        }
        self._client = switch[self._protocol]()

    def get(self, name):
        return self._client.get(name)

    def set(self, name, value):
        return self._client.set(name, value)

    def setex(self, name, time, value):
        return self._client.setex(name, time, value)

    def delete(self, *names):
        return self._client.delete(*names)


class SessionFactory(object):
    def __init__(self):
        pass

    @classmethod
    def create_redis(cls, url=None, **kwargs):
        if not url:
            return
        return Redis().init(url=url, **kwargs)

    @classmethod
    def create_member(cls, config):
        pass

    @classmethod
    def create_file(cls, config):
        pass
