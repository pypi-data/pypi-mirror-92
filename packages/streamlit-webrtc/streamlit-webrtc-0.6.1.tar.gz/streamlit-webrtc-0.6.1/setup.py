# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_webrtc']

package_data = \
{'': ['*']}

install_requires = \
['aiortc>=1.0.0', 'streamlit>=0.73.0']

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'streamlit-webrtc',
    'version': '0.6.1',
    'description': '',
    'long_description': '# streamlit-webrtc\n\n![PyPI](https://img.shields.io/pypi/v/streamlit-webrtc)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/streamlit-webrtc)\n![PyPI - License](https://img.shields.io/pypi/l/streamlit-webrtc)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/streamlit-webrtc)\n\n[![GitHub Sponsors](https://img.shields.io/github/sponsors/whitphx?label=Sponsor%20me%20on%20GitHub%20Sponsors&style=social)](https://github.com/sponsors/whitphx)\n\n<a href="https://www.buymeacoffee.com/whitphx" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="180" height="50" ></a>\n\n## Example\nYou can try out the sample app using the following commands.\n```\n$ pip install streamlit-webrtc opencv-python\n$ streamlit run https://raw.githubusercontent.com/whitphx/streamlit-webrtc-example/main/app.py\n```\n\nYou can also try it out here: https://streamlit-webrtc-example.herokuapp.com/; however, it’s running on a very small Heroku instance on a free plan, and may not work well if multiple users access it at the same time.\n\nThe deployment of the above example app is managed in this repository: https://github.com/whitphx/streamlit-webrtc-example/.\n',
    'author': 'Yuichiro Tsuchiya',
    'author_email': 't.yic.yt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whitphx/streamlit-webrtc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
