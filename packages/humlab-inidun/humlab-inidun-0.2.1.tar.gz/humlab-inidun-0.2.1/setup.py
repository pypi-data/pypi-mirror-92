# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notebooks',
 'notebooks.co_occurrence',
 'notebooks.common',
 'notebooks.most_discriminating_words',
 'notebooks.pos_statistics',
 'notebooks.word_trends']

package_data = \
{'': ['*']}

install_requires = \
['bokeh',
 'click',
 'debugpy>=1.2.1,<2.0.0',
 'ftfy',
 'gensim',
 'humlab-penelope>=0.3.2,<0.4.0',
 'ipyaggrid',
 'ipyfilechooser>=0.4.0,<0.5.0',
 'ipywidgets>=7.5.1,<8.0.0',
 'jupyter',
 'jupyter-bokeh>=2.0.4,<3.0.0',
 'jupyterlab',
 'matplotlib',
 'memoization',
 'nltk',
 'pandas',
 'pandas-bokeh>=0.5.2,<0.6.0',
 'pandocfilters==1.4.2',
 'qgrid>=1.3.1,<2.0.0',
 'sidecar>=0.4.0,<0.5.0',
 'spacy',
 'textacy',
 'tqdm>=4.51.0,<5.0.0',
 'wordcloud']

setup_kwargs = {
    'name': 'humlab-inidun',
    'version': '0.2.1',
    'description': 'INIDUN research project text analysis tools and utilities',
    'long_description': '# The INIDUN Text Analytics Repository\n\n### Prerequisites\n\n### Installation\n\n### Note\n\n\n',
    'author': 'Roger Mähler',
    'author_email': 'roger.mahler@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://inidun.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.5',
}


setup(**setup_kwargs)
