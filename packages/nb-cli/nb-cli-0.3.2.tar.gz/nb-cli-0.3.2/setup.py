# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nb_cli', 'nb_cli.plugin.hooks', 'nb_cli.project.hooks']

package_data = \
{'': ['*'],
 'nb_cli': ['plugin/*',
            'plugin/{{cookiecutter.plugin_slug}}/*',
            'plugin/{{cookiecutter.plugin_slug}}/plugins/*',
            'project/*',
            'project/{{cookiecutter.project_slug}}/*',
            'project/{{cookiecutter.project_slug}}/{{cookiecutter.source_dir}}/plugins/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'cookiecutter>=1.7.2,<2.0.0',
 'nonebot2>=2.0.0-alpha.7,<3.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'pyinquirer==1.0.3']

extras_require = \
{'deploy': ['docker-compose>=1.27.2,<2.0.0'],
 'docker': ['docker-compose>=1.27.2,<2.0.0']}

entry_points = \
{'console_scripts': ['nb = nb_cli.__main__:main']}

setup_kwargs = {
    'name': 'nb-cli',
    'version': '0.3.2',
    'description': 'CLI for nonebot2',
    'long_description': '# nb-cli\n\nCLI for nonebot2\n\nFeatures:\n\n- Create A NoneBot Project\n- Run NoneBot\n- Deploy NoneBot to Docker\n- Plugin Management\n  - Create new plugins\n  - Search for NoneBot Plugins Published on Official Store\n  - Install NoneBot Plugin Published on Official Store\n\n## How to use\n\n### Installation\n\n```shell\npip install nb-cli\n```\n\nor, with optional `deploy` dependency\n\n```shell\npip install nb-cli[deploy]\n```\n\n### Command-line usage\n\n```shell\nnb --help\n```\n\n### Interactive mode usage\n\n```shell\nnb\n```\n\n### CookieCutter usage\n\nCreating a project\n\n```shell\npip install cookiecutter\ncookiecutter https://github.com/yanyongyu/nb-cli.git --directory="nb_cli/project"\n```\n',
    'author': 'yanyongyu',
    'author_email': 'yanyongyu_1@126.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nonebot/nb-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
