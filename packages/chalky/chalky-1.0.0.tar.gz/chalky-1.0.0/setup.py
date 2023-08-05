# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['chalky', 'chalky.interface', 'chalky.shortcuts']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chalky',
    'version': '1.0.0',
    'description': 'Simple ANSI terminal text coloring',
    'long_description': '![Chalky](https://github.com/stephen-bunn/chalky/raw/master/docs/source/_static/assets/img/Chalky.png)\n\n[![Supported Versions](https://img.shields.io/pypi/pyversions/chalky.svg)](https://pypi.org/project/chalky/)\n[![Test Status](https://github.com/stephen-bunn/chalky/workflows/Test%20Package/badge.svg)](https://github.com/stephen-bunn/chalky)\n[![Documentation Status](https://readthedocs.org/projects/chalky/badge/?version=latest)](https://chalky.readthedocs.io/)\n[![Codecov](https://codecov.io/gh/stephen-bunn/chalky/branch/master/graph/badge.svg?token=G3KRpTeg5J)](https://codecov.io/gh/stephen-bunn/chalky)\n[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n> Simple ANSI terminal text coloring\n\nYet another terminal text coloring library…\n\nWhy? Because, I like certain things and I hate certain things about the currently\navailable solutions.\nThis here is my attempt to build an interface for simply applying ANSI escape sequences\nto strings that I enjoy and can update at my own free will.\nThat is it, there is nothing new or interesting that this packages adds.\nThanks 🎉\n\nFor more interesting details, please visit the\n[documentation](https://chalky.readthedocs.io/).\n\n## Style Composition\n\n```python\nfrom chalky import sty, fg\n\nmy_style = sty.bold & fg.red\nprint(my_style | "This is red on black")\nprint(my_style.reverse | "This is black on red")\n```\n\n![Basic Colors](https://github.com/stephen-bunn/chalky/raw/master/docs/source/_static/assets/img/basic.png)\n\n## Style Chaining\n\n```python\nfrom chalky import chain\n\nprint(chain.bold.green | "I\'m bold green text")\nprint(chain.white.bg.red.italic | "I\'m italic white text on a red background")\n```\n\n![Style Colors](https://github.com/stephen-bunn/chalky/raw/master/docs/source/_static/assets/img/chaining.png)\n\n## Truecolor\n\n```python\nfrom chalky import rgb, sty, hex\n\nprint(rgb(23, 255, 122) & sty.italic | "Truecolor as well")\nprint(sty.bold & hex("#ff02ff") | "More and more colors")\n```\n\n![True Colors](https://github.com/stephen-bunn/chalky/raw/master/docs/source/_static/assets/img/truecolor.png)\n\n## Disable Colors\n\n```python\nfrom chalky import configure, fg\n\nprint(fg.red | "I am red text")\nconfigure(disable=True)\nprint(fg.red | "I am NOT red text")\n```\n\n![Configure](https://github.com/stephen-bunn/chalky/raw/master/docs/source/_static/assets/img/configure.png)\n',
    'author': 'Stephen Bunn',
    'author_email': 'stephen@bunn.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stephen-bunn/chalky',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
