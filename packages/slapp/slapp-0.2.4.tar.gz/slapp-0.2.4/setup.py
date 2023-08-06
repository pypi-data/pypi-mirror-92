# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slapp']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.12,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'confuse>=1.4.0,<2.0.0',
 'marko>=1.0.1,<2.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['slapp = slapp.main:app']}

setup_kwargs = {
    'name': 'slapp',
    'version': '0.2.4',
    'description': 'Tool for easy deploying projects to git repo.',
    'long_description': '# Släpp\n\nTool for quick taggin and deploying releases to Git. Släpp automatically generates and pushes CHANGELOG file to your repo, based on your commit history.\n\n### Installation\n```bash\npip install slapp\n```\n\n### Usage\n- init slapp config\n```bash\nslapp init\n```\n- edit slapp.yml file if needed\n- do some stuff in your repo and commit it with * \n```bash\ngit add . && git commit -m "* Added some cool features!"\n```\n- release tag and build auto-changelog in one command\n```bash\nslapp release v0.1\n```\n\n',
    'author': 'm.semenov',
    'author_email': '0rang3max@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
