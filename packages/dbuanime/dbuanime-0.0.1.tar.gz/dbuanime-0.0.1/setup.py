# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dbuanime']
setup_kwargs = {
    'name': 'dbuanime',
    'version': '0.0.1',
    'description': 'Поиск Аниме/Манги по: Жанру,Рандому,Топу по годам.',
    'long_description': None,
    'author': 'DarsoX',
    'author_email': 'darsox.anime@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
