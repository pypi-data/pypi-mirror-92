# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylottie']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.0,<10', 'pyppeteer>=0.2.4,<2']

entry_points = \
{'console_scripts': ['pylottie = pylottie:cli']}

setup_kwargs = {
    'name': 'pylottie',
    'version': '2021.2.1',
    'description': 'Convert .tgs and .lottie to .webp or .gif using pyppeteer.',
    'long_description': '[![GitHub top language](https://img.shields.io/github/languages/top/FHPythonUtils/PyLottie.svg?style=for-the-badge)](../../)\n[![Codacy grade](https://img.shields.io/codacy/grade/[projid].svg?style=for-the-badge)](https://www.codacy.com/gh/FHPythonUtils/PyLottie)\n[![Repository size](https://img.shields.io/github/repo-size/FHPythonUtils/PyLottie.svg?style=for-the-badge)](../../)\n[![Issues](https://img.shields.io/github/issues/FHPythonUtils/PyLottie.svg?style=for-the-badge)](../../issues)\n[![License](https://img.shields.io/github/license/FHPythonUtils/PyLottie.svg?style=for-the-badge)](/LICENSE.md)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/FHPythonUtils/PyLottie.svg?style=for-the-badge)](../../commits/master)\n[![Last commit](https://img.shields.io/github/last-commit/FHPythonUtils/PyLottie.svg?style=for-the-badge)](../../commits/master)\n[![PyPI Downloads](https://img.shields.io/pypi/dm/pylottie.svg?style=for-the-badge)](https://pypi.org/project/pylottie/)\n[![PyPI Version](https://img.shields.io/pypi/v/pylottie.svg?style=for-the-badge)](https://pypi.org/project/pylottie/)\n\n<!-- omit in TOC -->\n# PyLottie\n\n<img src="readme-assets/icons/name.png" alt="Project Icon" width="750">\n\nConvert .tgs and .lottie to .webp or .gif using pyppeteer.\n\n- [Docs](#docs)\n- [Formats](#formats)\n- [Install With PIP](#install-with-pip)\n- [Language information](#language-information)\n\t- [Built for](#built-for)\n- [Install Python on Windows](#install-python-on-windows)\n\t- [Chocolatey](#chocolatey)\n\t- [Download](#download)\n- [Install Python on Linux](#install-python-on-linux)\n\t- [Apt](#apt)\n- [How to run](#how-to-run)\n\t- [With VSCode](#with-vscode)\n\t- [From the Terminal](#from-the-terminal)\n- [Download](#download-1)\n\t- [Clone](#clone)\n\t\t- [Using The Command Line](#using-the-command-line)\n\t\t- [Using GitHub Desktop](#using-github-desktop)\n\t- [Download Zip File](#download-zip-file)\n- [Community Files](#community-files)\n\t- [Licence](#licence)\n\t- [Changelog](#changelog)\n\t- [Code of Conduct](#code-of-conduct)\n\t- [Contributing](#contributing)\n\t- [Security](#security)\n\n## Docs\nSee the [Docs](/DOCS/README.md) for more information.\n\n\n\n\n## Formats\n\n|Format|Animated|\n|------|--------|\n|.gif  |✔      |\n|.webp |✔      |\n\n\n## Install With PIP\n\n```python\npip install pylottie\n```\n\nHead to https://pypi.org/project/pylottie/ for more info\n\n\n## Language information\n### Built for\nThis program has been written for Python 3 and has been tested with\nPython version 3.9.0 <https://www.python.org/downloads/release/python-380/>.\n\n## Install Python on Windows\n### Chocolatey\n```powershell\nchoco install python\n```\n### Download\nTo install Python, go to <https://www.python.org/> and download the latest\nversion.\n\n## Install Python on Linux\n### Apt\n```bash\nsudo apt install python3.9\n```\n\n## How to run\n### With VSCode\n1. Open the .py file in vscode\n2. Ensure a python 3.9 interpreter is selected (Ctrl+Shift+P > Python:Select\nInterpreter > Python 3.9)\n3. Run by pressing Ctrl+F5 (if you are prompted to install any modules, accept)\n### From the Terminal\n```bash\n./[file].py\n```\n\n\n## Download\n### Clone\n#### Using The Command Line\n1. Press the Clone or download button in the top right\n2. Copy the URL (link)\n3. Open the command line and change directory to where you wish to\nclone to\n4. Type \'git clone\' followed by URL in step 2\n```bash\n$ git clone https://github.com/FHPythonUtils/PyLottie\n```\n\nMore information can be found at\n<https://help.github.com/en/articles/cloning-a-repository>\n\n#### Using GitHub Desktop\n1. Press the Clone or download button in the top right\n2. Click open in desktop\n3. Choose the path for where you want and click Clone\n\nMore information can be found at\n<https://help.github.com/en/desktop/contributing-to-projects/cloning-a-repository-from-github-to-github-desktop>\n\n### Download Zip File\n\n1. Download this GitHub repository\n2. Extract the zip archive\n3. Copy/ move to the desired location\n\n## Community Files\n### Licence\nMIT License\n(See the [LICENSE](/LICENSE.md) for more information.)\n\n### Changelog\nSee the [Changelog](/CHANGELOG.md) for more information.\n\n### Code of Conduct\nIn the interest of fostering an open and welcoming environment, we\nas contributors and maintainers pledge to make participation in our\nproject and our community a harassment-free experience for everyone.\nPlease see the\n[Code of Conduct](https://github.com/FHPythonUtils/.github/blob/master/CODE_OF_CONDUCT.md) for more information.\n\n### Contributing\nContributions are welcome, please see the [Contributing Guidelines](https://github.com/FHPythonUtils/.github/blob/master/CONTRIBUTING.md) for more information.\n\n### Security\nThank you for improving the security of the project, please see the [Security Policy](https://github.com/FHPythonUtils/.github/blob/master/SECURITY.md) for more information.\n',
    'author': 'FredHappyface',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FHPythonUtils/PyLottie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
