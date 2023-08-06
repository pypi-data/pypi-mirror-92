# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['royalnet',
 'royalnet.alchemist',
 'royalnet.engineer',
 'royalnet.lazy',
 'royalnet.lazy.tests',
 'royalnet.royaltyping',
 'royalnet.scrolls']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0', 'sqlalchemy>=1.3.19,<2.0.0', 'toml>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'royalnet',
    'version': '6.0.1',
    'description': 'A multipurpose bot framework',
    'long_description': '# `royalnet` 6\n\nThe repository for the development of `royalnet` version `6.0.0` and later.\n\nThe documentation is [hosted on Read The Docs](https://royalnet-6.readthedocs.io/en/latest/).\n\n## See also\n\n### PDA implementations\n\n- [royalnet-discordpy](https://github.com/Steffo99/royalnet-discordpy) (based on a Discord Bot)\n- [royalnet-console](https://github.com/Steffo99/royalnet-console) (based on a terminal session)\n\n### Old Royalnet versions\n\n- [Royalnet 5](https://github.com/Steffo99/royalnet-5)\n- [Royalnet 4](https://github.com/Steffo99/royalnet-5/tree/four)\n- [Royalbot 3](https://github.com/Steffo99/royalbot-3)\n- [Royalbot 2](https://github.com/Steffo99/royalbot-2)\n- [Royalbot 1](https://github.com/Steffo99/royalbot-1)\n',
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Steffo99/royalnet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
