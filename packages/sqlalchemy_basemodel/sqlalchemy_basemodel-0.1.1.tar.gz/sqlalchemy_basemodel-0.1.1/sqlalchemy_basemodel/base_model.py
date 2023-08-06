from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
from .utils import classproperty


def do_nothing(self, *args, **kwargs):
    pass


def get_commit_method(session):
    def __commit(self, *args, **kwargs):
        if not kwargs.get('commit', True):
            return
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
    return __commit


def get_save_method(session):
    def save(self, *args, **kwargs):
        self.before_save(*args, **kwargs)
        session.add(self)
        self.__commit(*args, **kwargs)
        self.after_save(*args, **kwargs)
        return self
    return save


def get_delete_method(session):
    def delete(self, *args, **kwargs):
        self.before_delete(*args, **kwargs)
        session.delete(self)
        self.__commit(*args, **kwargs)
        self.after_delete(*args, **kwargs)
        del self
    return delete


def get_update_method():
    def update(self, *args, **kwargs):
        self.before_update(*args, **kwargs)
        self.updated_at = datetime.now()
        self.__commit(*args, **kwargs)
        self.after_update(*args, **kwargs)
        return self
    return update


def create_base_model_class(base, session):
    return type('Model', (base, ), {
        '__abstract__': True,
        'id': Column(Integer, primary_key=True, autoincrement=True),
        'created_at': Column(DateTime(timezone=True), default=datetime.now()),
        'updated_at': Column(DateTime(timezone=True), default=datetime.now()),
        '__tablename__': classproperty(lambda cls: cls.__name__.lower() + 's'),
        'query': classproperty(lambda cls: session.query(cls)),
        'before_save': do_nothing,
        'after_save': do_nothing,
        'before_update': do_nothing,
        'after_update': do_nothing,
        'before_delete': do_nothing,
        'after_delete': do_nothing,
        '__commit': get_commit_method(session),
        'save': get_save_method(session),
        'delete': get_delete_method(session),
        'update': get_update_method()
    })
