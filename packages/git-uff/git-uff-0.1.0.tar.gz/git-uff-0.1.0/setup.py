# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_uff']

package_data = \
{'': ['*']}

install_requires = \
['gitpython>=3.1.12,<4.0.0']

entry_points = \
{'console_scripts': ['git-uff = git_uff.main:main']}

setup_kwargs = {
    'name': 'git-uff',
    'version': '0.1.0',
    'description': 'Prints the forge url for a given file of a Git repository checkout',
    'long_description': '# git-uff\n\nPrints the forge URL for a given file of a Git repository checkout.\n\n## Intro\n\nHave you ever been discussing with colleagues over IRC/Slack/Matrix/whatever about source code and found yourself needing to point them to a particular file in a git repository?\n\nThis is tedious to do.\n\nOne solution is to tell them the path in their checkout, hoping they are on the same branch as you.\n\nAnother solution is to point your browser to the forge hosting your git repository, select the right branch, navigate the file hierarchy, find your file and copy the file URL.\n\nA better (in my opinion 😉) solution is to use `git-uff`. This tool adds an `uff` (short for "URL for file") git sub-command, which takes the path to a file in your repository checkout and prints the matching forge URL.\n\nFor example to print the URL of the `src/linux/nanonote.desktop` file from my [Nanonote][] project:\n\n```\n$ git uff src/linux/nanonote.desktop\nhttps://github.com/agateau/nanonote/blob/master/src/linux/nanonote.desktop\n```\n\n[Nanonote]: https://github.com/agateau/nanonote\n\nYou can also point them to a specific line with the `-l` argument:\n\n```\n$ git uff src/linux/nanonote.desktop -l 10\nhttps://github.com/agateau/nanonote/blob/master/src/linux/nanonote.desktop#L10\n```\n\n## But my code is not on GitHub...\n\n`git-uff` is not tied to GitHub. It supports GitLab, SourceHut and a few others. For now the supported forges are hard-coded in the code, but making it configurable should be easy.\n\n## Installation\n\nThe simplest solution is to use [pipx][]:\n\n```\npipx install git-uff\n```\n\n[pipx]: https://github.com/pipxproject/pipx\n\n## License\n\nApache 2.0\n',
    'author': 'Aurélien Gâteau',
    'author_email': 'mail@agateau.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agateau/git-uff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
