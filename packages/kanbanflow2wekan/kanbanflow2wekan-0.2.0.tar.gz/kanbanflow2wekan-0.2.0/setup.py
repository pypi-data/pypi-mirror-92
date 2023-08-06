# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kanbanflow2wekan']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'kanbanflow2wekan',
    'version': '0.2.0',
    'description': 'This is a library to perform kanban migration from Kanbanflow to Wekan in an automated way.',
    'long_description': 'Kanbanflow2Wekan\n================\n\n[![](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/download/releases/3.4.0/)  [![](https://img.shields.io/github/license/ResidentMario/missingno.svg)](https://github.com/mdiniz97/AnsibleAWX-Client/blob/master/README.md)\n\n\nDonate to help keep this project maintained\n\n<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ZHX5884XX26MW&source=url" target="_blank">\n    <img src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />\n</a>\n\nSummary\n-------\nThis is a library to perform kanban migration from Kanbanflow to Wekan in an automated way.\n\nRequirements\n------------\n* requests\n\nQuick Start Guide\n-----------------\n\n### Install kanbanflow2wekan\n\tpip install kanbanflow2wekan\n\n### Initialize kanbanflow2wekan\n\n\n    import os\n    from dotenv import load_dotenv\n    from kanbanflow2wekan import k2w\n\n    load_dotenv()\n\n    print(\'kanbanflow2wekan | by: @mdiniz97\\n\\n\')\n\n    migration = k2w(\n        os.getenv(\'WEKAN_URL\'),\n        os.getenv(\'WEKAN_USER\'),\n        os.getenv(\'WEKAN_PASSWORD\'),\n        os.path.join(os.getcwd(), \'kanbanflow\'),\n        os.getenv(\'KANBANFLOW_USER\'),\n        os.getenv(\'KANBANFLOW_PASSWORD\'),\n        kf_download_attachments=True,\n    )\n\n    migration.migrate()\n',
    'author': 'mdiniz97',
    'author_email': 'marcosdinizpaulo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mdiniz97/kanbanflow2wekan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
