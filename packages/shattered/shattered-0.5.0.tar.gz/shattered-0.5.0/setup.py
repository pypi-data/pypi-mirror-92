# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['shattered']

package_data = \
{'': ['*']}

install_requires = \
['stomp.py>=6.0.0,<7.0.0']

entry_points = \
{'console_scripts': ['shattered = shattered.cli:main']}

setup_kwargs = {
    'name': 'shattered',
    'version': '0.5.0',
    'description': 'STOMP meets bottle.py',
    'long_description': '# Shattered\n\nSTOMP meets `bottle.py`\n\n[![Build Status](https://travis-ci.com/bradshjg/shattered.svg?branch=master)](https://travis-ci.com/bradshjg/shattered)\n\n## Getting Started\n\n### Installation\n\n`pip install shattered`\n\n### CLI\n\n`shattered run` will run a Shattered app, using one of the following (in order):\n\n1. The `--app` flag.\n2. The `SHATTERED_APP` environment variable.\n3. `app.py` as the application module name.\n\nUse `shattered config` to see the current configuration (same app resolution as `run` command).\n\n### Echo Server\n\n`app.py`\n\n```python\nimport logging\n\nfrom shattered import Shattered\n\n\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(__name__)\n\napp = Shattered(host="rabbitmq")\n\n\n@app.subscribe("/queue/echo")\ndef echo(headers, body, conn):\n    logger.info("%s %s", headers, body)\n\n\n@app.subscribe("/queue/echo")\ndef echo_fancy(headers, body, conn):\n    logger.info("✨✨✨%s %s✨✨✨", headers, body)\n\n\napp.run()\n```\n\n#### Running the Demo\n\nStart up RabbitMQ using `docker-compose up`\n\nIn another shell, run `docker-compose run shattered python examples/echo/echo.py`\n\nIn another shell, run `docker-compose run shattered python examples/echo/send.py`\n',
    'author': 'Jimmy Bradshaw',
    'author_email': 'james.g.bradshaw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bradshjg/shattered',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
