from skyext.exts import db, session_redis, cache, es


def init_component(config):
    if not config:
        return

    db.init(config)
    session_redis.init(config)
    es.init(config)
    cache.init(config)
