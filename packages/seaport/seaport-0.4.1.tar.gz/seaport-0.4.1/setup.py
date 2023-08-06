# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seaport',
 'seaport.clipboard',
 'seaport.clipboard.portfile',
 'seaport.pull_request']

package_data = \
{'': ['*'], 'seaport': ['autocomplete/*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['seaport = seaport.init:seaport']}

setup_kwargs = {
    'name': 'seaport',
    'version': '0.4.1',
    'description': 'A more mighty port bump',
    'long_description': '🌊 seaport\n==========\n\n|ci-badge| |rtd-badge| |cov-badge|\n\nA more mighty `port bump` for `MacPorts <https://www.macports.org>`_!\n\n.. code-block::\n\n    > seaport clip gping\n    🌊 Starting seaport...\n    👍 New version is 1.2.0-post\n    🔻 Downloading from https://github.com/orf/gping/tarball/v1.2.0-post/gping-1.2.0-post.tar.gz\n    🔎 Checksums:\n    Old rmd160: 8b274132c8389ec560f213007368c7f521fdf682\n    New rmd160: 4a614e35d4e1e496871ee2b270ba8836f84650c6\n    Old sha256: 1879b37f811c09e43d3759ccd97d9c8b432f06c75a27025cfa09404abdeda8f5\n    New sha256: 1008306e8293e7c59125de02e2baa6a17bc1c10de1daba2247bfc789eaf34ff5\n    Old size: 853432\n    New size: 853450\n    ⏪️ Changing revision numbers\n    No changes necessary\n    📋 The contents of the portfile have been copied to your clipboard!\n\n✨ Features\n-----------\n\n* **Automatically determines new version numbers and checksums** for MacPorts portfiles.\n* **Copies the changes to your clipboard 📋**, and optionally **sends a PR to update them**.\n* Contains **additional checking functionality**, such as running tests, linting and installing the updated program.\n* `PEP 561 compatible <https://www.python.org/dev/peps/pep-0561>`_, with built in support for type checking.\n\nTo find out more, please read the `Documentation <http://seaport.rtfd.io/>`_.\n\nInstallation\n------------\n\nNaturally, MacPorts needs to already be installed for the tool to function.\n\nHomebrew 🍺\n***********\n\nFor those with both Homebrew and MacPorts installed, you can run the following:\n\n.. code-block::\n\n    brew install harens/tap/seaport\n\nBinary bottles are provided for x86_64_linux, catalina and big_sur.\n\n.. note::\n    ⚠️ You can install the development version by running the following:\n\n    .. code-block::\n\n        brew install harens/tap/seaport --HEAD\n\nPyPi 🐍\n********\n\nIf you install seaport via `PyPi <https://pypi.org/project/seaport/>`_ and you want it to send PRs for you, please install `GitHub CLI <https://cli.github.com>`_.\n\n.. code-block::\n\n    pip3 install seaport\n\n🔨 Contributing\n---------------\n\n- Issue Tracker: `<https://github.com/harens/seaport/issues>`_\n- Source Code: `<https://github.com/harens/seaport>`_\n\nAny change, big or small, that you think can help improve this project is more than welcome 🎉.\n\nAs well as this, feel free to open an issue with any new suggestions or bug reports. Every contribution is appreciated.\n\n©️ License\n----------\n\nSimilar to other MacPorts-based projects, seaport is licensed under the `BSD 3-Clause "New" or "Revised" License <https://github.com/harens/seaport/blob/master/LICENSE>`_.\n\n📒 Notice of Non-Affiliation and Disclaimer\n-------------------------------------------\n\nThis project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with the MacPorts Project, or any of its subsidiaries or its affiliates. The official MacPorts Project website can be found at `<https://www.macports.org>`_.\n\nThe name MacPorts as well as related names, marks, emblems and images are registered trademarks of their respective owners.\n\n.. |ci-badge| image:: https://img.shields.io/github/workflow/status/harens/seaport/Tests?logo=github&style=flat-square\n   :target: https://github.com/harens/seaport/actions\n   :alt: GitHub Workflow Status\n.. |rtd-badge| image:: https://img.shields.io/readthedocs/seaport?logo=read%20the%20docs&style=flat-square\n   :target: https://seaport.rtfd.io/\n   :alt: Read the Docs\n.. |cov-badge| image:: https://img.shields.io/codecov/c/github/harens/seaport?logo=codecov&style=flat-square\n   :target: https://codecov.io/gh/harens/seaport\n   :alt: Codecov\n',
    'author': 'harens',
    'author_email': 'harensdeveloper@gmail.com',
    'maintainer': 'harens',
    'maintainer_email': 'harensdeveloper@gmail.com',
    'url': 'https://github.com/harens/seaport',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
