# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiny_router', 'tiny_router.simple_regex']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'tiny-router',
    'version': '0.0.8',
    'description': 'Tiny HTTP router',
    'long_description': '# tiny-router\n\n[![PyPI](https://img.shields.io/pypi/v/tiny-router)](https://pypi.org/project/tiny-router/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tiny-router)](https://pypi.org/project/tiny-router/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![license](https://img.shields.io/github/license/nekonoshiri/tiny-router)](https://github.com/nekonoshiri/tiny-router/blob/main/LICENSE)\n\nTiny HTTP router.\n\n## Usage\n\n```Python\nfrom tiny_router import SimpleRouter\n\nrouter = SimpleRouter()\n\n\n@router.get("/users/{user_id}")\ndef get_user(params):\n    if params.get("user_id") == 1:\n        return {"id": 1, "name": "Alice"}\n\n\nroute = router.resolve("GET", "/users/{user_id}")\nuser = route({"user_id": 1})\n\nassert user == {"id": 1, "name": "Alice"}\n```\n\nMore examples are in `examples/` directory of\n[repository](https://github.com/nekonoshiri/tiny-router).\n\n## Features\n\n- `SimpleRouter`: exact-match router\n- `SimpleRegexRouter`: simple regex-based router\n- Abstract `Router`: user can implement their own routers\n- Support for type hints\n\n## API\n\n### Module `tiny_router`\n\nTODO\n\n',
    'author': 'Shiri Nekono',
    'author_email': 'gexira.halen.toms@gmail.com',
    'maintainer': 'Shiri Nekono',
    'maintainer_email': 'gexira.halen.toms@gmail.com',
    'url': 'https://github.com/nekonoshiri/tiny-router',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
