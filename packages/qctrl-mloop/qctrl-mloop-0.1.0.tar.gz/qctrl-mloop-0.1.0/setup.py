# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qctrlmloop']

package_data = \
{'': ['*']}

install_requires = \
['M-LOOP>=3.2.1,<3.3.0',
 'numpy>=1.18,<2.0',
 'qctrl>=8.6.1,<9.0.0',
 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'qctrl-mloop',
    'version': '0.1.0',
    'description': 'Q-CTRL Python M-LOOP',
    'long_description': '# Q-CTRL Python M-LOOP\n\nThe Q-CTRL Python M-LOOP package allows you to integrate BOULDER OPAL\nautomated closed-loop optimizers with automated closed-loop optimizations\nmanaged by the open-source package M-LOOP.\n',
    'author': 'Q-CTRL',
    'author_email': 'support@q-ctrl.com',
    'maintainer': 'Q-CTRL',
    'maintainer_email': 'support@q-ctrl.com',
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.4,<3.9',
}


setup(**setup_kwargs)
