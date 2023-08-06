from ext.db.main import DBInit

DB = None


def create_db(config):
    _db_url = config.SQLALCHEMY_DATABASE_URI
    if not _db_url:
        return

    _instance = DBInit()
    _instance.init_engine(url=_db_url)
    return _instance
