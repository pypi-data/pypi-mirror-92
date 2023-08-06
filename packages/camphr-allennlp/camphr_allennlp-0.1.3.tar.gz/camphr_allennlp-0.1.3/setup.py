# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camphr_allennlp']

package_data = \
{'': ['*']}

install_requires = \
['allennlp>=1.0.0,<=1.0.1',
 'boto3>=1.14.44,<2.0.0',
 'camphr>=0.7.0,<0.8',
 'unofficial-udify==0.2.1']

entry_points = \
{'spacy_factories': ['elmo = camphr_allennlp:Elmo.from_nlp',
                     'udify = camphr_allennlp:Udify.from_nlp']}

setup_kwargs = {
    'name': 'camphr-allennlp',
    'version': '0.1.3',
    'description': 'AllenNLP plugin for camphr',
    'long_description': '',
    'author': 'Yohei Tamura',
    'author_email': 'tamuhey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PKSHATechnology-Research/camphr-allennlp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
