import redis


class Redis(object):
    def __init__(self):
        self.url = None
        self._client = None

    def init(self, url=None, **kwargs):
        if not url:
            return

        self.url = url
        self._client = redis.from_url(self.url)

    def get(self, name):
        return self._client.get(name)

    def set(self, name, value):
        return self._client.set(name, value)

    def setex(self, name, time, value):
        return self._client.setex(name, time, value)

    def delete(self, *names):
        return self._client.delete(*names)

    def save(self):
        return self._client.save()

    def keys(self, pattern='*'):
        return self._client.keys(pattern)


