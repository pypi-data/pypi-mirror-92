# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skippex']

package_data = \
{'': ['*']}

install_requires = \
['PlexAPI>=4.2.0,<5.0.0',
 'PyChromecast>=7.7.1,<8.0.0',
 'pid>=3.0.4,<4.0.0',
 'requests>=2.25.1,<3.0.0',
 'typing-extensions>=3.7.4,<4.0.0',
 'websocket_client>=0.57.0,<0.58.0',
 'wrapt>=1.12.1,<2.0.0',
 'xdg>=5.0.1,<6.0.0',
 'zeroconf>=0.28.8,<0.29.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'console_scripts': ['skippex = skippex.cmd:main']}

setup_kwargs = {
    'name': 'skippex',
    'version': '0.2.3',
    'description': "Automatic 'skip intro' for Plex with Chromecast support",
    'long_description': '# Skippex\n\nSkippex skips intros automatically for you on Plex, with support for the\nChromecast.\n\n**IMPORTANT NOTE**: This is still pretty much beta software. Expect bugs and\nplease report them!\n\n## Installation\n\nInstalling Skippex through **Docker** is the easiest way to get started:\n\n```console\n$ docker pull ghcr.io/sprt/skippex\n```\n\n*Docker-compose example coming soon.*\n\nIf you prefer not to use Docker, you can also use [**pipx**][pipx], which will\ninstall Skippex in its own virtual environment:\n\n```console\n$ pipx install skippex\n```\n\nOr you can just use **pip**:\n\n```console\n$ pip install --user skippex\n```\n\n[pipx]: https://pipxproject.github.io/pipx/\n\n## Usage\n\nThe first time you use Skippex, you\'ll first have to authorize the application\nwith Plex using the following command. This will open a new tab in your Web\nbrowser allowing you to authenticate and authorize the application to access\nyour Plex account.\n\n<table>\n  <tr>\n    <th>Docker</th>\n    <th>pipx & pip</th>\n  </tr>\n  <tr>\n    <td>\n      <code>$ docker run -v skippex:/config --network host ghcr.io/sprt/skippex auth</code>\n    </td>\n    <td>\n      <code>$ skippex auth</code>\n    </td>\n  </tr>\n</table>\n\nOnce that\'s done, you can simply run Skippex and it\'ll start monitoring your\nplayback sessions and automatically skip intros for you on supported devices:\n\n<table>\n  <tr>\n    <th>Docker</th>\n    <th>pipx & pip</th>\n  </tr>\n  <tr>\n    <td>\n      <code>$ docker run -v skippex:/config --network host ghcr.io/sprt/skippex run</code>\n    </td>\n    <td>\n      <code>$ skippex run</code>\n    </td>\n  </tr>\n</table>\n\nEt voilà! When this command says "Ready", Skippex is monitoring your shows and\nwill automatically skip intros for you.\n\n*Note: Due to a [Chromecast limitation][cast-diff-subnets], the Docker container\nhas to run with host mode networking.*\n\n[cast-diff-subnets]: https://www.home-assistant.io/integrations/cast#docker-and-cast-devices-and-home-assistant-on-different-subnets\n\n## Things to know\n\n * **Clients need to have "Advertise as player" enabled.**\n * Only works for players on the local network.\n * Only skips once per playback session.\n * Solely based on the intro markers detected by Plex; Skippex does not attempt\n   to detect intros itself.\n\n## Tested and supported players\n\n * Plex Web App\n * Plex for iOS (both iPhone and iPad)\n * Chromecast v3\n\nThe NVIDIA SHIELD might be supported as well, but I don\'t have one so I can\'t\ntest it. Other players might also be supported. In any case, please inform me\nby [creating a new issue][new_issue], so I can add your player to this list.\n\n[new_issue]: https://github.com/sprt/skippex/issues/new\n\n## Known issues\n\n * With a Chromecast, when seeking to a position, the WebSocket only receives\n   the notification 10 seconds later. Likewise, the HTTP API starts returning\n   the correct position only after 10 seconds. This means that if, before the\n   intro, the user seeks to within 10 seconds of the intro, they may view it for\n   a few seconds (before the notification comes in and saves us).\n\n   One workaround would be to listen to Chromecast status updates using\n   `pychromecast`, but that would necessitate a rearchitecture of the code.\n',
    'author': 'sprt',
    'author_email': 'hellosprt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sprt/skippex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
