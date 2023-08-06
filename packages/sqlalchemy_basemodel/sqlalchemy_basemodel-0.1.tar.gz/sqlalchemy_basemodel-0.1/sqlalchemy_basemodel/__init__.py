from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .base_model import create_base_model_class


class SQLAlchemy:
    def __init__(self, database: str, debug: bool):
        self.engine = create_engine(database, echo=debug)
        self.base = declarative_base()
        self.Session = sessionmaker(bind=self.engine)
        self.Model = create_base_model_class(self.base, self.Session())

    def create_all(self):
        self.base.metadata.create_all(self.engine)
