from skyext.cache import Cache
from skyext.alchemy_db import DataBase
from skyext.db.es_db import ElasticSearch
from skyext.session import Session

db = DataBase()
cache = Cache()
session_redis = Session()
es = ElasticSearch()
