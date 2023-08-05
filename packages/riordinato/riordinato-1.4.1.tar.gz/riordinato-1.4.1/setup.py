# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['riordinato']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'riordinato',
    'version': '1.4.1',
    'description': 'organize your files with prefixes',
    'long_description': '# Riordinato\n\nRiordinato is a python library for organizing files with prefixes.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install riordinato.\n\n```bash\npip install riordinato \n```\n\n## Usage\n\nRiordinato is used to organize files by prefixes. For example, we want to move the files that have python in their name to the python folder and similar with the files that have work.\n\n```\n/home/user/documents\n    ├── pythonWork.py\n    ├── python_examples.txt\n    ├── family.jpg\n    ├── dog.png\n    ├── index.html\n    ├── work_list.txt\n    ├── any_work.docx\n    ├── python_exercise.pdf\n    ├── work_for_later.docx\n    │\n    ├── python/\n    └── work/\n```\n\nFirst import riordinato\n\n```py\nfrom riordinato import Riordinato\n```\n\nDefine a directory where we have the files we want to move.\n\n```py\npath = \'/home/user/documents\'\n```\n\nCreate the instance.\n\n```py\norganize = Riordinato(path)\n```\n\nIf you want to see the files that are in the path you can print the files attribute.\n\n```py\n>>> print(organize.files)\n\n[\'pythonWork.py\', \'python_examples.txt\', \'family.jpg\', \'dog.png\', \'index.html\', \n\'work_list.txt\', \'any_work.docx\', \'work_for_later.docx\', \'python_exercise.pdf\']\n```\n\nNow you have to create a prefix. to do it is the same when you create a new item for a dictionary, the key is the prefix and the value is the destination\n\n```py\norganize.prefixes[\'python\'] = \'./python\'\norganize.prefixes[\'work\'] = \'./work\' \n```\n\nTo organize our files we use the moveFiles method\n\n```py\norganize.movefiles()\n```\n\nAnd our directory would look like this.\n\n```\n/home/user/documents\n    ├── family.jpg\n    ├── dog.png\n    ├── index.html\n    ├── any_work.docx          \n    │\n    ├── python/\n    │   ├── python_exercise.pdf\n    │   ├── pythonWork.py\n    │   └── python_examples.txt\n    └── work/\n        ├── work_for_later.docx\n        └── work_list.txt\n```\n\nIf we want to move files with a specific prefix, use the "specific" parameter of the method.\n\n```py\norganize.movefiles(specific=\'python\')\n```\n\n```\n/home/user/documents\n    ├── family.jpg\n    ├── dog.png\n    ├── index.html\n    ├── work_list.txt\n    ├── work_for_later.docx\n    ├── any_work.docx\n    │\n    ├── python/\n    │   ├── python_exercise.pdf\n    │   ├── pythonWork.py\n    │   └── python_examples.txt\n    └── work/\n```\n\nYou can also ignore files that contain a certain prefix. In this case we will ignore the files that contain the python prefix.\n\n```py\norganize.movefile(ignore=\'python\')\n```\n\n```\n/home/user/documents\n    ├── pythonWork.py\n    ├── python_examples.txt\n    ├── family.jpg\n    ├── dog.png\n    ├── index.html\n    ├── any_work.docx\n    ├── python_exercise.pdf\n    │\n    ├── python/\n    └── work/\n        ├── work_for_later.docx\n        └── work_list.txt\n```\n\n> **_NOTE:_** the specific and ignore parameters are also compatible with lists.\n\n## Contributing\nA contributing.md will be added soon.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Dan-',
    'author_email': 'misternutel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DAN-pix/Riordinato',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
