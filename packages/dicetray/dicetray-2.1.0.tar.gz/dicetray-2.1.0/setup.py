# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dicetray']

package_data = \
{'': ['*']}

install_requires = \
['sly>=0.4,<0.5']

setup_kwargs = {
    'name': 'dicetray',
    'version': '2.1.0',
    'description': 'Tabletop RPG Dice roller',
    'long_description': "Dicetray\n========\n\n.. image:: https://github.com/gtmanfred/dicetray/workflows/Tests/badge.svg\n    :target: https://github.com/gtmanfred/dicetray\n\n.. image:: https://img.shields.io/codecov/c/github/gtmanfred/dicetray\n    :target: https://codecov.io/gh/gtmanfred/dicetray\n\n.. image:: https://img.shields.io/pypi/v/dicetray\n    :target: https://pypi.org/project/dicetray\n\n.. image:: https://img.shields.io/pypi/l/dicetray\n    :target: http://www.apache.org/licenses/LICENSE-2.0\n\n.. image:: https://img.shields.io/pypi/dm/dicetray\n    :target: https://pypi.org/project/dicetray/\n\n\nTabletop RPG Dice rolling manager for handling `Standard Dice Notation`_\n\nGrammer\n-------\n\nBelow is the grammer that is used by the parser generator to intepret inputs.\n\n    statement : expr\n              | expr PLUS expr\n              | expr MINUS expr\n              | expr TIMES expr\n              | expr DIVIDE expr\n\n    expr : NUMBER\n         | dice\n         | func\n\n    func : dice\n         | dice KEEPHIGH\n         | dice KEEPLOW\n         | dice DROPHIGH\n         | dice DROPLOW\n         | dice KEEPHIGH NUMBER\n         | dice KEEPLOW NUMBER\n         | dice DROPHIGH NUMBER\n         | dice DROPLOW NUMBER\n\n    dice : NUMBER DIE NUMBER\n         | NUMBER DIE TYPE\n\n    PLUS : +\n    MINUS : -\n    TIMES : *\n    DIVIDE : /\n\n    NUMBER: [0-9]+\n    TYPE: [fF%]\n    DIE : d\n    KEEPHIGH: kh\n    KEEPLOW: kl\n    DROPHIGH: dh\n    DROPLOW: dl\n\nExample\n-------\n\n.. code-block:: python\n\n    >>> from dicetray import Dicetray\n    >>> Dicetray('1d20 + 3').roll()\n    15\n    >>> Dicetray('4d6dl').roll()\n    10\n    >>> Dicetray('4d6kh3').roll()\n    12\n    >>> d = Dicetray('2d20kh + 1d4 + 3')\n    >>> d.result\n    >>> d.dice\n    set()\n    >>> d.roll()\n    18\n    >>> d.dice\n    {<Dice (d20): 14>, <Dice (d20): 14>, <Dice (d4): 1>}\n    >>> d.result\n    18\n\n.. _Standard Dice Notation: https://en.wikipedia.org/wiki/Dice_notation\n",
    'author': 'Daniel Wallace',
    'author_email': 'danielwallace@gtmanfred.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gtmanfred/dicetray.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
