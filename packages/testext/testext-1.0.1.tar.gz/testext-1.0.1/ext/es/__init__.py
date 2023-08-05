from ext.es.main import ESTool

ES = None


def create_es(config):
    _hosts = config.ELASTICSEARCH_HOST
    if not _hosts:
        return

    _instance = ESTool()
    _instance.init_app(_hosts)

    return _instance
