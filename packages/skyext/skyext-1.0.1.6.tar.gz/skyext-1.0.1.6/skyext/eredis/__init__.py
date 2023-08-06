import redis

REDIS = None


def create_redis(redis_url):
    if not redis_url:
        return

    redis_host_port_db = str(redis_url).replace("redis://", "")
    if redis_host_port_db.find("/"):
        _host_port, _db = redis_host_port_db.split("/")
        _host, _port = _host_port.split(":")
    else:
        _db = 0
        _host, _port = redis_host_port_db.split(":")

    _instance = redis.Redis(host=_host, port=_port, db=int(_db), decode_responses=True)
    return _instance
