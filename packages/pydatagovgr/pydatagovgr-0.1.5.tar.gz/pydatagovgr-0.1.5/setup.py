# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydatagovgr']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<2.26.0']

setup_kwargs = {
    'name': 'pydatagovgr',
    'version': '0.1.5',
    'description': 'A Pythonic client for the official https://data.gov.gr API.',
    'long_description': "# pydatagovgr\n\n[![PyPI](https://img.shields.io/pypi/v/pydatagovgr)](https://pypi.org/project/pydatagovgr/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydatagovgr)](https://www.python.org/) [![codecov](https://codecov.io/gh/ilias-ant/pydatagovgr/branch/main/graph/badge.svg?token=2H0VB8I8IH)](https://codecov.io/gh/ilias-ant/pydatagovgr) [![PyPI - Wheel](https://img.shields.io/pypi/wheel/pydatagovgr)](https://www.python.org/dev/peps/pep-0427/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ilias-ant/pydatagovgr/Python%20package)](https://github.com/ilias-ant/pydatagovgr/actions?query=workflow%3A%22Python+package%22)\n\n\nAn unofficial Pythonic client for the official [data.gov.gr](https://data.gov.gr) API. Aims to be an easy, intuitive and out-of-the-box way to:\n\n- find data published by central government, local authorities and public bodies of Greece\n- build related products and services.\n\nwhile being robust, following best-practices and eliminating developer-induced bugs.\n\nThe aspiration for this library is to enable users of different backgrounds (academia, industry, students etc.) with \nan interest to programmatically explore and utilize the open data of data.gov.gr, to do so without having to write-debug-maintain trivial code \nor worry about that.\n\n## Install\n\nThe recommended installation is via `pip`:\n\n```bash\npip install pydatagovgr\n```\n\n## Quick Usage\n\nYou must have an account on [data.gov.gr](https://data.gov.gr) to use the API service. In order to register and request\nan API token, submit a request in the designated official form [here](https://data.gov.gr/token/). The procedure is very \nsimple and takes less than 5 minutes.\n\n```python\nfrom pydatagovgr import DataGovClient\n\n\ngov_client = DataGovClient(token='xoxb-1234-1243')\n\n# fetch the COVID-19 vaccination data\ncovid_data = gov_client.query('mdg_emvolio')\n\n# fetch data on Greece's internet traffic\ntraffic_data = gov_client.query('internet_traffic')\n\n# fetch a list of the forest fires\nfire_data = gov_client.query('mcp_forest_fires')\n```\n\n## Features\n\nThe `pydatagovgr` client supports out-of-the-box all the things you know (and love), such as:\n\n- **authentication**: properly handles the authentication to data.gov.gr - all you have to do is provide a valid token. \n- **persistent session**: making several requests to data.gov.gr reuses the same underlying connection.\n- **timeout policy**: the client will stop waiting for a response from data.gov.gr after some time. Defaults to 10 sec.\n- **retry policy**: to account for potential server failures of lossy network connections, client automatically retries \n  with an exponential-backoff, to avoid harming the data.gov.gr. Defaults to a maximum of 3 retries.\n\nAlso, this library comes with extensive test coverage (100%) of the core functionality. The test suite will constantly\nimprove towards the v1 version.\n\n## Not-So-Quick Usage\n\nThe data.gov.gr API is currently organized into endpoints called **datasets**, each available via the `query` endpoint.\n\nThe `pydatagovgr` client provides a corresponding `query` method, through which every available dataset can be obtained.\nYou can also pass additional arguments to filter the results accordingly. \n\n```python\nfrom pydatagovgr import DataGovClient\n\n\ngov_client = DataGovClient(token='xoxb-1234-1243')\n\n# fetch the COVID-19 vaccination data for the 2021\ndata = gov_client.query('mdg_emvolio', date_from='2021/01/01', date_to='2021/12/31')\n```\nYou can also use Python objects as arguments:\n\n```python\nimport datetime\n\n\ndata = gov_client.query('mdg_emvolio', \n                        date_from=datetime.date(2021, 1, 1), \n                        date_to=datetime.date(1, 12, 31))\n```\n\nApart from the authentication token, you can also configure the timeout and retry policies of your client. For example: \n\n```python\nfrom pydatagovgr import DataGovClient\n\n\n# this client will stop waiting for a response after 7 seconds \ngov_client = DataGovClient(token='xoxb-1234-1243', timeout=7)\n\n# this client will retry at most 3 times, with an exponential-backoff\n# (i.e. each retry waits exponentially longer before occurs: 1, 2, 4, 8, 16, 32, 64, ... seconds)\ngov_client = DataGovClient(token='xoxb-1234-1243', max_retries=3)\n\n# this client will respect both a timeout policy and a retry policy\ngov_client = DataGovClient(token='xoxb-1234-1243', timeout=7, max_retries=3)\n```\n\n## How to contribute\n\nIf you wish to contribute, [this](CONTRIBUTING.md) is a great place to start!\n\n## License\n\nDistributed under the [MIT License](LICENSE).\n\n## Acknowledgements\n\nAll rights are reserved by the official https://data.gov.gr site, its developers, its maintainers and the \nHellenic Government.\n",
    'author': 'ilias-ant',
    'author_email': 'ilias.antonopoulos@yahoo.gr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/pydatagovgr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
