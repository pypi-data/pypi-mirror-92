# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jadoc', 'jadoc.mecab', 'jadoc.word']

package_data = \
{'': ['*']}

install_requires = \
['mecab-python3>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'jadoc',
    'version': '0.2.3',
    'description': 'Tokenizes Japanese documents to enable CRUD operations.',
    'long_description': '# Jadoc: Tokenizes Japanese Documents to Enable CRUD Operations\n\n[![PyPI Version](https://img.shields.io/pypi/v/jadoc.svg)](https://pypi.org/pypi/jadoc/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/jadoc.svg)](https://pypi.org/pypi/jadoc/)\n[![License](https://img.shields.io/pypi/l/jadoc.svg)](https://github.com/poyo46/jadoc/blob/main/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\n## Installation\n\n**Install MeCab**\n\nMeCab is required for Jadoc to work.\nIf it is not already installed, [install MeCab](https://taku910.github.io/mecab/) first.\n\n**Install Jadoc**\n\n```console\n$ pip install jadoc\n```\n\n## Examples\n\n```python\nfrom jadoc.doc import Doc\n\n\ndoc = Doc("本を書きました。")\n\n# print surface forms of the tokens.\nsurfaces = [word.surface for word in doc.words]\nprint("/".join(surfaces))  # 本/を/書き/まし/た/。\n\n# print plain text\nprint(doc.get_text())  # 本を書きました。\n\n# delete a word\ndoc.delete(3)  # Word conjugation will be done as needed.\nprint(doc.get_text())  # 本を書いた。\n\n# update a word\nword = doc.conjugation.tokenize("読む")\n# In addition to conjugation, transform the peripheral words as needed.\ndoc.update(2, word)\nprint(doc.get_text())  # 本を読んだ。\n```\n',
    'author': 'poyo46',
    'author_email': 'poyo4rock@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/poyo46/jadoc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
