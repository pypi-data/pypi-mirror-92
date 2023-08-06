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
        _redis_configs = config.REDIS
        if not _redis_configs:
            return

        ret_redis_config = dict()
        for _redis_config in _redis_configs:
            if _redis_config:
                _redis = create_redis(_redis_configs[_redis_config])
                if _redis:
                    ret_redis_config[_redis_config] = _redis

        EXT_CONTEXT["redis"] = ret_redis_config

    if not EXT_CONTEXT.get("es"):
        _es = create_es(config)
        EXT_CONTEXT["es"] = _es
