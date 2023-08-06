from skyext.cache import Cache
from skyext.alchemy_db import DB
from skyext.db.es_db import ES
from skyext.session import Session

db = DB()
cache = Cache()
session_redis = Session()
es = ES()
