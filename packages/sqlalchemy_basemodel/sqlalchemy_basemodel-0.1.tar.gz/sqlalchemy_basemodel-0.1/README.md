# sqlalchemy-basemode
Маленькая надстройка над sqlalchemy, добавляющая BaseModel


# Установка
`pipenv install sqlalchemy_basemodel`

# Пример использования

```python
from sqlalchemy_basemodel import SQLAlchemy
from sqlalchemy import Column, String


db = SQLAlchemy(database='sqlite:///:memory:', debug=False)


class User(db.Model):
    username = Column('Ник', String)


db.create_all()


User(username='w0rng').save()

user = User.query.first()

user.username = 'sqlalchemy_basemodel'
user.update()

user = User.query.all()[0]
user.delete()
```
