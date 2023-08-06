from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='sqlalchemy_basemodel',
    version='0.1',
    packages=find_packages(),
    # long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=[
        'SQLAlchemy>=1.3.22'
    ]
)
