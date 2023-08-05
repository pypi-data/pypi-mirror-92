# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['papi_sdk',
 'papi_sdk.endpoints',
 'papi_sdk.exceptions',
 'papi_sdk.models',
 'papi_sdk.models.order_booking_finish',
 'papi_sdk.models.order_info',
 'papi_sdk.models.search',
 'papi_sdk.models.search.hotelpage',
 'papi_sdk.models.search.hotels',
 'papi_sdk.models.search.region',
 'papi_sdk.tests',
 'papi_sdk.tests.mocked_data']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'papi-sdk',
    'version': '1.1.1',
    'description': 'pAPI SDK is a Python SDK for ETG APIv3',
    'long_description': '# pAPI SDK\n\n![main workflow](https://github.com/emergingtravel/papi-sdk-python/workflows/Main/badge.svg)\n![pypi version](https://img.shields.io/pypi/v/papi-sdk.svg)\n![pypi downloads](https://img.shields.io/pypi/dm/papi-sdk.svg)\n![python versions](https://img.shields.io/pypi/pyversions/papi-sdk.svg)\n![license](https://img.shields.io/github/license/emergingtravel/papi-sdk-python.svg)\n\npAPI SDK is a python SDK for [ETG APIv3](https://docs.emergingtravel.com/).\nThe abbreviation "pAPI" stands for "Partner API". \n\n## Requirements\n\n- Python 3.6+\n- requests\n- pydantic\n\n## Installation\n\n```\npip install papi-sdk\n```\n\n## Quickstart\n\nTo start using ETG APIv3 you need a key, which you received after registration. \nA key is a combination of an `id` and `uuid`. These are passed into each request as a Basic Auth header after initialization.\n`APIv3` supports all arguments provided by [requests](https://github.com/psf/requests), ex. `timeout`.\n\n```python\nfrom papi_sdk import APIv3\n\n\npapi = APIv3(key=\'1000:022a2cf1-d279-02f3-9c3c-596aa09b827b\', timeout=15)\n```\n\nThen you can use all available methods. Say you want to check an overview of the available methods (which is `api/b2b/v3/overview` endpoint), you do:\n\n```python\noverview = papi.overview(timeout=1)\n```\n\nAnother example is downloading hotels dump with `api/b2b/v3/hotel/info/dump` endpoint:\n\n```python\ndata = HotelInfoDumpRequest(language=\'ru\')\ndump = papi.get_hotel_info_dump(data=data)\nprint(dump.data.url)\n```\n\nNote: if you don\'t provide your headers and specifically your `User-Agent` in requests options then it will be automatically added, ex. `papi-sdk/v1.0.2 requests/2.25.1 (python/3.8)`\n',
    'author': 'Stanislav Losev',
    'author_email': 'stanislav.losev@ostrovok.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/emergingtravel/papi-sdk-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
