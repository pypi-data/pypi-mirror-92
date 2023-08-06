# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['docker_amend']
install_requires = \
['docker>=4.2.0,<5.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['docker-amend = docker_amend:_run']}

setup_kwargs = {
    'name': 'docker-amend',
    'version': '0.1.2',
    'description': 'Amend Docker images by running a command in a separate layer.',
    'long_description': "# docker-amend\n\nAmend Docker images by running a command in a temporary container.\n\n```console\n$ pipx install docker-amend  # (plain `pip` works too)\n$ docker-amend [OPTIONS] IMAGE[:VERSION] COMMAND...\n```\n\n## Description\n\ndocker-amend lets you modify an IMAGE by running COMMAND inside a temporary container.\nYou can use it to add dependencies to your project without rebuilding the whole image\nfrom ground.\n\nThis is basically `docker run` and `docker commit` in one go, but easier to use.\n\n## Options\n\n* `-t, --tag NAME[:VERSION]`: Use a different name/tag for the resulting image.\n* `-v, --volume SOURCE[:TARGET[:MODE]]`: Bind mount a volume.\n* `--no-cwd-volume`: Do not mount current working directory as a volume.  [default: False]\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n## Example\n\nLet's say you're making a Python app:\n\n```console\n$ docker build -t my-image .\n\n... (some development goes on, then:)\n\n$ docker-amend my-image poetry add requests\n$ docker run my-image poetry show\nrequests         2.23.0     Python HTTP for Humans.\n$ grep requests pyproject.toml\nrequests = ^2.23.0\n```\n",
    'author': 'Alexander Pushkov',
    'author_email': 'alexander@notpushk.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/notpushkin/docker-amend',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
