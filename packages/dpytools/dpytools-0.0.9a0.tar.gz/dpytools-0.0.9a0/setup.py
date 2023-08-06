# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dpytools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dpytools',
    'version': '0.0.9a0',
    'description': 'Simple tools to build discord bots using discord.py',
    'long_description': '# dpytools\nToolset to speed up developing discord bots using discord.py\n\n<hr>\n\n## Status of the project\n\nEarly development. As such its expected to be unstable and unsuited for production.\n\n## Components\n\n**Module** | **Functions** | **Notes**\n--- | --- | --- \nmenus | arrows  | Dispays a menu made from passed Embeds with navigation by reaction.\n.| confirm | Returns the user reaction to confirm or deny a passed message.\nembeds | paginate_to_embeds | Paginates a long text into a list of embeds.\nparsers| parse_time | Parses strings with the format "2h15m" to a timedelta object.\nowner_cog | - | collection of useful commands for the bot owner.\nMore to come... \n\n<hr>\n\n# Contributing\nFeel free to make a pull request.',
    'author': 'chrisdewa',
    'author_email': 'alexdewa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chrisdewa/dpytools',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
