# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soccerapi', 'soccerapi.api', 'soccerapi.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'soccerapi',
    'version': '0.7.0',
    'description': 'A simple python wrapper to get soccer odds',
    'long_description': "# soccerapi\n\n[![PyPI version](https://badge.fury.io/py/soccerapi.svg)](https://badge.fury.io/py/soccerapi)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nsoccerapi (Application Programming Interface) is a simple wrapper build on top\nof some bookmakers (888sport, bet365 and Unibet) in order to get data about\nsoccer (aka football) odds using python commands.\n\n## ⚽️ The goal\n\nThe goal of the project is provided an enjoyable way to get odds data for\ndifferent soccer leagues. Usually, if someone wants to get these types of data,\nhave to build by him self (and from scratch) a program able to scrape the\nbetting site or use some kind paid API. Soccer API try to address this problem.\n\n## 💡 The philosophy\n\nKeep it simple. Simple API, simple http requests, few dependencies. In the past\nI have tried to build some heavy framework able to scraping site (using\nselenium able to handle complex JavaScript): was an *unmaintainable nightmare*.\n\n## 📘 The documentation\n\nThe following section contain all the useful information to use this API at\nits best. Read it carefully.\n\n### Installation\n\nUse your favorite python package manager (like *pip*, *pipenv*, *poetry*). For\nexample if you use *pip* type in your terminal:\n\n```bash\npip install soccerapi\n```\n\n------------------------------------------------------------------------------\n\nAlternatively, if you want a kind of testing/developing setup, you can install\nSoccer API directly from source code by first cloning the repository from\ngithub and then install dev dependencies\n([poetry](https://python-poetry.org/) is required)\n\n```bash\ngit clone https://github.com/S1M0N38/soccerapi.git\ncd soccerapi\npoetry install\n```\n\nand then activate the environment\n\n```bash\npoetry shell\n```\n\n### Usage\n\nImport the *soccerapi* bookmaker, define the *api* variable and request\n*odds*.\n\n```python\nfrom soccerapi.api import Api888Sport\n# from soccerapi.api import ApiUnibet\n# from soccerapi.api import ApiBet365\n\napi = Api888Sport()\nurl = 'https://www.888sport.com/#/filter/football/italy/serie_a'\nodds = api.odds(url)\n\nprint(odds)\n```\n\n```python\n[\n  {\n    'time': '2020-01-12T19:45:00Z'\n    'home_team': 'Roma',\n    'away_team': 'Juventus',\n    'both_teams_to_score': {'no': 2380, 'yes': 1560},\n    'double_chance': {'12': 1320, '1X': 1710, '2X': 1360},\n    'full_time_resut': {'1': 3200, '2': 2160, 'X': 3450},\n  },\n\n  ...\n\n  {\n    'time': '2020-01-13T19:45:00Z'\n    'home_team': 'Parma',\n    'away_team': 'Lecce',\n    'both_teams_to_score': {'no': 2280, 'yes': 1600},\n    'double_chance': {'12': 1270, '1X': 1270, '2X': 1960},\n    'full_time_resut': {'1': 1850, '2': 3850, 'X': 3800},\n  }\n]\n```\n\nThe *odds* method return a list of next events of the request competition\n(in the example: the url points to *italy-serie_a*, try to open on your\nbrowser). To get these url, open the bookmaker site and browser to competitions\nyou want to scrape: that's the urls you have to pass to *odds()*.\n\nFor example urls for *england-premier_league* are:\n\n- **bet365** `https://www.bet365.it/#/AC/B1/C1/D13/E51761579/F2/`\n- **888sport** `https://www.888sport.com/#/filter/football/england/premier_league`\n- **unibet** `https://www.unibet.com/betting/sports/filter/football/england/premier_league/matches`\n\n(note that these are urls that works for me, maybe your urls are not `.it` but\n`.com`)\n\n### Country restriction\n\nThe regulation of online gambling varies from country to country. There are\ndifferent versions of the betting site depending on the provenience of your\nhttp request. Moreover, most bookmakers implement some kind of VPN detection\nthat block VPN-http requests. Due to this constrains it's difficult to test\nsoccerapi for worldwide usability. Here is reported some results about bookmaker\naccessibility from various country.\n\n|            | bet365 | 888sport / unibet |\n|----------- | :----: | :---------------: |\n|accessible  | :it: :brazil:  | :us: :canada: :australia: :brazil: :switzerland: :it: :de: :denmark: :es: :finland: :jp: :netherlands: :norway: :sweden: :ireland: :india: :singapore: :hong_kong: :new_zealand: :mexico: :romania:|\n|inaccessible|        | :fr: :uk:         |\n\n### Contributing\n\nIf you like to contribute to the project read\n[CONTRIBUTING.md](https://github.com/S1M0N38/soccerapi/blob/master/CONTRIBUTING.md)\n",
    'author': 'S1M0N38',
    'author_email': 'bertolottosimone@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/S1M0N38/soccerapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
