# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogram_media_group', 'aiogram_media_group.storages']

package_data = \
{'': ['*']}

install_requires = \
['aiogram>=2.11.2,<3.0.0']

setup_kwargs = {
    'name': 'aiogram-media-group',
    'version': '0.2.0',
    'description': 'AIOGram handler for media groups (also known as albums)',
    'long_description': '# aiogram-media-group\nAIOGram handler for media groups (also known as albums)\n\n### Features\n- Memory and Redis storage drivers supported\n- Ready to work with multiple bot instances\n\n### Install\n\n```bash\npip install aiogram-media-group\n# or\npoetry add aiogram-media-group\n```\n\n### Usage\n\nMinimal usage example:\n```python\nfrom aiogram_media_group import MediaGroupFilter, media_group_handler\n\n@dp.message_handler(MediaGroupFilter(), content_types=ContentType.PHOTO)\n@media_group_handler\nasync def album_handler(messages: List[types.Message]):\n    for message in messages:\n        print(message)\n```\n\nCheckout [echo-bot](./examples/echo.py) for complete usage example ',
    'author': 'deptyped',
    'author_email': 'deptyped@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/deptyped/aiogram-media-group',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
