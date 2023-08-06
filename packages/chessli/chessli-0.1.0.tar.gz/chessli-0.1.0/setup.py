# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chessli', 'chessli.cli']

package_data = \
{'': ['*']}

install_requires = \
['berserk>=0.10.0,<0.11.0',
 'matplotlib>=3.3.3,<4.0.0',
 'omegaconf>=2.0.6,<3.0.0',
 'pandas>=1.2.0,<2.0.0',
 'python-chess>=1.999,<2.0',
 'rich>=9.9.0,<10.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['chessli = chessli.cli.main:app']}

setup_kwargs = {
    'name': 'chessli',
    'version': '0.1.0',
    'description': 'A free and open source chess improvement app that combines the power of lichess and anki',
    'long_description': '\n# Chessli\n\n![GitHub Repo\nstars](https://img.shields.io/github/stars/pwenker/chessli?style=social)\n![GitHub code size in\nbytes](https://img.shields.io/github/languages/code-size/pwenker/chessli)\n![Lines of\ncode](https://img.shields.io/tokei/lines/github/pwenker/chessli)\n![GitHub last\ncommit](https://img.shields.io/github/last-commit/pwenker/chessli)\n![GitHub\nissues](https://img.shields.io/github/issues-raw/pwenker/chessli)\n![GitHub\nfollowers](https://img.shields.io/github/followers/pwenker?style=social)\n\n![Thumbnail](https://github.com/pwenker/chessli/blob/main/imgs/chessli.png?raw=true)\n\n***A free and open-source CHESS improvement program that combines the power\nof Lichess and Anki.***\n\n## Demos\n\n### CLI Demo (watch whole video on [Youtube](https://www.youtube.com/embed/XbD71Kq7cx4))\n\n![CLI DEMO GIF](https://github.com/pwenker/chessli/blob/main/imgs/chessli_cli_demo.gif?raw=true)\n\n### Anki Cards Demo (watch whole video on [Youtube](https://www.youtube.com/embed/aj-FqJhPyyA))\n\n![CLI CARDS GIF](https://github.com/pwenker/chessli/blob/main/imgs/chessli_cards_demo.gif?raw=true)\n\n## Documentation\nIf you have a question please first take a look at the [documentation](https://www.pwenker.com/posts/chess/chessli/home/) (also available [here](https://www.pwenker.com/chessli)), which is currently work in progress.\nFeel free to open an [issue](https://github.com/pwenker/chessli/issues/new) afterwards :).\n\n\n## Features\n\n- **Automatically fetch your games** and played tactics puzzles from [`lichess`](https://www.lichess.org) via the [`berserk`](https://github.com/rhgrant10/berserk) python client for the Lichess API.!\n- **Find your mistakes** by parsing your games and analysing them with [`python-chess`](https://github.com/niklasf/python-chess).\n- **Create a simple opening repertoire**!\n- **Spaced repetition & Retrieval Practice**: Automatically  (via [`apy`](https://github.com/lervag/apy)) add your game mistakes, your openings and your tackled lichess puzzles to [`Anki`](https://apps.ankiweb.net/).\n- More features on the way...!\n\n\n## Getting Started\n:information_source: **Information**\n- At the moment, some technical expertise is needed to use `Chessli`.\n- Starting with version 0.2, however, I will add an Anki-Addon to ease those technical hurdles.\n- Also, please notice that this is a very early version, and some code parts are still rough on the edges.\n- Further, there are still some opinionated parts and hard-coded choices:\n  - For example, it is not possible to fetch more than 20 games at once (to not bug down Lichess).\n  - A lot more options are going to be opened up as soon as the codebase stabilises.\n- *Long story short*: things will improve over time! But feel free to open up issues!\n\n### Get Chessli\n\n1. Clone this repository & navigate into it:\n\n```console\ngit clone https://github.com/pwenker/chessli.git && cd chessli\n```\n\n2. Install chessli with `pip`:\n\n```console\npip install -e .\n```\n\n### Anki Support via `apy`\n\n- In order to directly "ankify" your mistakes, openings and tactics, you need to set up [`apy`](https://github.com/lervag/apy/).\n- Currently `chessli` is compatible with `apy` version 0.6.0 and `anki` version 2.1.26.\n- Please refer to its [install instructions](https://github.com/lervag/apy/#install-instructions) for detailed information.\n\n### Lichess API Authentification\n\n- Some parts of the lichess API, for example fetching your puzzle activity, require authentification.\n- For this purpose, you need to get a [personal API access token](https://lichess.org/account/oauth/token).  Put your token into `configs/lichess.token`.\n- For more information read the [corresponding `berserk` documentation section](https://berserk.readthedocs.io/en/master/usage.html#authenticating).\n\n### Get the Chessli Anki Cards\n\n- There is no dedicated shared deck page on Anki available yet, but will be coming soon.\n- Until then, download the required sample of Anki cards from [here]("/imgs/Chessli Sample Cards.apkg").\n\n*Acknowledgments*:\n\n- The interactive chess functionality on the cards is taken from [these fantastic cards](https://ankiweb.net/shared/info/1082754005).\n- You can find a great video about those cards [here](https://www.youtube.com/watch?v=uxSP1YkfD0k&feature=youtu.be).\n\n\n## Basic Usage\nTo get an overview of the basic CLI capabilities of `Chessli`, take a look at this short demo video I\ncreated (click on the image below to watch on youtube):\n\n### Youtube-Video: CLI Demo\n[![Chessli CLI Demo](https://img.youtube.com/vi/XbD71Kq7cx4/0.jpg)](https://www.youtube.com/embed/XbD71Kq7cx4)\n\nThere is also a short video showing the `chessli`s Anki cards in action:\n\n### Youtube-Video: Anki Cards Demo\n[![Chessli Anki Cards Demo](https://img.youtube.com/vi/aj-FqJhPyyA/0.jpg)](https://www.youtube.com/embed/aj-FqJhPyyA)\n\n:information_source: I am in the midst of creating a comprehensive documentation that will be released with version 0.2.\n\nUntil then you can take a look at the [CLI documentation](docs/cli.md), or programmatically ask it questions:\n\n**Examples**:\n\n- Getting general help for `chessli`:\n\n```console\nchessli --help\n```\n- Getting help for individual `chessli` commands:\n\n```console\nchessli games --help\n```\n\n- You can add a create a file `configs/lichess.user` and put your user name in it.\n- Then it will be used as default username in place of mighty `DrNykterstein`.\n\n## Acknowledgments\n\n- **Lichess**:\n  - A free, no-ads, open source chess server that let\'s everyone play chess!\n  - I truly love it.\n  - Think about whether to [become a patron](https://lichess.org/patron)! :)\n- **Anki**:\n  - A free and open-source flashcard program using spaced-repetition, a technique from cognitive science for fast and long-lasting memorization.\n  - I couldn\'t imagine learning without it anymore.\n- **Anki Cards Design**\n  - The interactive chess functionality on the cards is taken from [these fantastic cards](https://ankiweb.net/shared/info/1082754005).\n  - You can find a great video about those cards [here](https://www.youtube.com/watch?v=uxSP1YkfD0k&feature=youtu.be).\n- **Further Awesome Tools**:\n  - Most of the heavy lifting, e.g. parsing games, finding mistakes, extracting openings, etc. is done with `python-chess`.\n  - The communication between `lichess` and `chessli` is done via `berserk`.\n  - The CLI is built with `typer`.\n  - The rich colors are made possible with `rich`.\n  - The `apy` tool is used to programmatically import the chess knowledge into Anki.\n  - **You should really check those tools out; each and everyone one of them is amazing.**\n',
    'author': 'Pascal Wenker',
    'author_email': 'pwenker@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pwenker/chessli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
