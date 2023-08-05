import redis

REDIS = None


def create_redis(config):
    _redis_config = config.REDIS
    if not _redis_config:
        return

    _host = _redis_config.get("HOST")
    _port = _redis_config.get("PORT")

    _instance = redis.Redis(host=_host, port=_port, decode_responses=True)
    return _instance
