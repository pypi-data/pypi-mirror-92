# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bestbuyapi', 'bestbuyapi.api', 'bestbuyapi.utils']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'bestbuyapi',
    'version': '2.0.0',
    'description': "Python Wrapper over Best Buy's REST API",
    'long_description': '---\nPython Best Buy API Wrapper\n---\n\n![image](https://img.shields.io/badge/version-2.0.0-blue.svg)\n\n[![image](https://travis-ci.com/lv10/bestbuyapi.svg?branch=master)](https://travis-ci.com/lv10/bestbuyapi)\n\nThis is a small python wrapper implementation for BestBuy API. This\nimplementation does not cover all the APIs from BestBuy yet. As of now,\nit only supports the calls to the Products, Categories, bulk and Cover\nAPIs. Locations and Reviews API are in the making.\n\nThe wrapper doesn\\\'t assume any design requirements on the user end.\nQueries to the API endpoints are done similar to what you would put in\nthe browser with the convenience of having python prepare for you the\nquery, url, and interpret the response.\n\nNOTICE: This project is only supported by python 3.6, 3.7, 3.8. If you\nneed support for an older version of python3, please reach out to me.\n\n# Features\n\n- Query Bulk BestBuy API\n- Query Stores BestBuy API (by id, currently)\n- Query Products BestBuy API\n- Query Categories BestBuy API\n- Obtain queries result in JSON or XML\n\nFor details on how to use the Best Buy API go to:\n<https://developer.bestbuy.com/documentation>\n\n# Install\n\n```{.sourceCode .python}\n$ pip install BestBuyAPI\n```\n\n**How to use Product, Category, Store and Bulk APIs**\n\n```{.sourceCode .python\n>>> from bestbuy import BestBuyAPI\n>>> bb = BestBuyAPI("YourSecretAPIKey")\n>>>\n>>> a_prod = bb.products.search(query="sku=9776457", format="json")\n>>> a_cat = bb.category.search_by_id(category_id="abcat0011001", format="json")\n>>> all_categories = bb.bulk.archive("categories", "json")}\n```\n\n# FAQ\n\n- Is there any difference between /api.bestbuy.com/ and\n  api.remix.bestbuy.com?\n\n  A:// This is the response from BestBuy Dev department: \\"There is no\n  difference, they serve the same data - we just consolidated domains.\n  The official url to use is api.bestbuy.com though.\\"\n\nAny questions please feel free to email me at: <luis@lv10.me>\n',
    'author': 'lv10',
    'author_email': 'luis@lv10.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lv10/bestbuyapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
