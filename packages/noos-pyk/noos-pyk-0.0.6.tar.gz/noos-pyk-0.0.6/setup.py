# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['noos_pyk', 'noos_pyk.clients']

package_data = \
{'': ['*']}

install_requires = \
['requests']

extras_require = \
{'websocket': ['websocket-client']}

setup_kwargs = {
    'name': 'noos-pyk',
    'version': '0.0.6',
    'description': 'A simple, yet useful Python toolkit',
    'long_description': '[![CircleCI](https://circleci.com/gh/noosenergy/noos-python-kit.svg?style=svg&circle-token=5c5370df196704b1e8a8dd7c6f2ec0731c154beb)](https://circleci.com/gh/noosenergy/noos-python-kit)\n\n# Noos Energy Python Toolkit\n\nThis is a simple, yet useful toolkit that supports you in writing microservices-style Python apps.\n\n## Installation\n\nPackage available from the [PyPi repository](https://pypi.org/project/noos-pyk/):\n\n    $ pip install noos-pyk\n\n## Usage as a library\n\nThe project currently houses a boilerplate to build Python clients for REST services.\n\nAs an example, to implement a Python client wrapping up HashiCorp\'s Terraform Cloud API,\n\n```python\n# Import the namespace within your project\nfrom noos_pyk.clients import auth, json\n\n\n# Define a bearer token authentication class\nclass TerraformAuth(auth.HTTPTokenAuth):\n    default_header = "Authorization"\n    default_value = "Bearer"\n\n\n# Wireup all components for a JSON REST client\nclass TerraformClient(json.JSONClient, auth.AuthClient):\n    default_base_url = "https://app.terraform.io/api/"\n    default_content_type = "application/vnd.api+json"\n\n    default_auth_class = TerraformAuth\n```\n\n## Development\n\nOn Mac OSX, make sure [poetry](https://python-poetry.org/) has been installed and pre-configured,\n\n    $ brew install poetry\n\nThis project is shipped with a Makefile, which is ready to do basic common tasks.\n\n```\n$ make\n\nhelp                           Display this auto-generated help message\nupdate                         Lock and install build dependencies\nclean                          Clean project from temp files / dirs\nformat                         Run auto-formatting linters\ninstall                        Install build dependencies from lock file\nlint                           Run python linters\ntest                           Run pytest with all tests\npackage                        Build project wheel distribution\nrelease                        Publish wheel distribution to PyPi\n```\n',
    'author': 'Noos Energy',
    'author_email': 'contact@noos.energy',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noosenergy/noos-python-kit',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
