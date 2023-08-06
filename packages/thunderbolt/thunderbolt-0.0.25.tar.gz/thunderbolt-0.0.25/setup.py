# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thunderbolt', 'thunderbolt.client']

package_data = \
{'': ['*']}

install_requires = \
['boto3', 'gokart', 'moto==1.3.6', 'tqdm']

setup_kwargs = {
    'name': 'thunderbolt',
    'version': '0.0.25',
    'description': 'gokart file downloader',
    'long_description': "# Thunderbolt\n\nThunderbolt is data manager for gokart.\n\n  \n [1] Auto loading gokart task logs  \n [2] Check task params using pandas  \n [3] Download data from python  \n  \n\n# Usage\n\n### install\n```\npip install thunderbolt\n```\n\n### Example\n\nIf you specify `TASK_WORKSPACE_DIRECTORY`, thunderbolt reads the log.  \nSo making tasks pandas.DataFrame, and load dumped data.  \nThis is also possible from S3 or GCS. (s3://~~, gs://~~)  \n  \nExample:\n```\nfrom thunderbolt import Thunderbolt\n\ntb = Thunderbolt()\nprint(tb.get_task_df())\nprint(tb.get_data('TASK_NAME'))\n```\n\nPlease look here too: https://github.com/m3dev/thunderbolt/blob/master/examples/example.ipynb  \n  \n\n# Thanks\n\n- `gokart`: https://github.com/m3dev/gokart\n",
    'author': 'vaaaaanquish',
    'author_email': '6syun9@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m3dev/thunderbolt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
