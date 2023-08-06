# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_webrtc']

package_data = \
{'': ['*']}

install_requires = \
['aiortc>=1.0.0', 'streamlit>=0.63']

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'streamlit-webrtc',
    'version': '0.6.0',
    'description': '',
    'long_description': '# streamlit-webrtc\n\n## Example\nYou can try out the sample app using the following commands.\n```\n$ pip install streamlit-webrtc opencv-python\n$ streamlit run https://raw.githubusercontent.com/whitphx/streamlit-webrtc-example/main/app.py\n```\n\nYou can also try it out here: https://streamlit-webrtc-example.herokuapp.com/; however, it’s running on a very small Heroku instance on a free plan, and may not work well if multiple users access it at the same time.\n\nThe deployment of the above example app is managed in this repository: https://github.com/whitphx/streamlit-webrtc-example/.\n',
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
