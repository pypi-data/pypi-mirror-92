from ext.db import create_db
from ext.es import create_es
from ext.redis import create_redis

EXT_CONTEXT = {

}


def create_ext(config):
    if not config:
        return

    global EXT_CONTEXT

    if not EXT_CONTEXT.get("db"):
        _db = create_db(config)
        EXT_CONTEXT["db"] = _db

    if not EXT_CONTEXT.get("redis"):
        _redis = create_redis(config)
        EXT_CONTEXT["redis"] = _redis

    if not EXT_CONTEXT.get("es"):
        _es = create_es(config)
        EXT_CONTEXT["es"] = _es
