from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class DBInit(object):
    def __init__(self):
        self.Model = None
        self.session_factory = None

    def init_engine(self, url=None, **kwargs):
        if kwargs:
            self.engine = create_engine(url, **kwargs)
        else:
            self.engine = create_engine(url)

        self.session_factory = sessionmaker(bind=self.engine)
        self.Model = declarative_base()
        self.Model.metadata.create_all(self.engine)

    @contextmanager
    def session_maker(self):
        if not self.session_factory:
            raise Exception("db initial error")

        try:
            session = self.session_factory()
            print("<<<<<<<<<<<<<<< start")
            yield session
            session.commit()
            print("<<<<<<<<<<<<<<< commit <<<<<<<<")
        except:
            session.rollback()
            print("<<<<<<<<<<<<<<< rollback <<<<<<<<")
            raise
        finally:
            session.close()
            print("<<<<<<<<<<<<<<< close <<<<<<<<")