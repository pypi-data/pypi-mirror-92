# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pigsqueeze']

package_data = \
{'': ['*']}

install_requires = \
['plum-py>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['psz = pigsqueeze.pigsqueeze:cli']}

setup_kwargs = {
    'name': 'pigsqueeze',
    'version': '1.0.0',
    'description': 'A library to write and read arbitrary data to and from image files. You probably already know why you need it.',
    'long_description': '# pigsqueeze\n[![CircleCI](https://circleci.com/gh/timwedde/pigsqueeze.svg?style=svg)](https://circleci.com/gh/timwedde/pigsqueeze)\n[![Downloads](https://pepy.tech/badge/pigsqueeze)](https://pepy.tech/project/pigsqueeze)\n\nA library to write and read arbitrary data to and from image files. You probably already know why you need it.\n\npigsuqeeze is a command line tool as well as a Python library for easily writing arbitrary to (and later retrieving it from) image files. Currently only JPEG is supported, but I\'m open to add support for more file formats, if they support this. It stores binary data in one or more chunks of app-specific data segments as enabled by the JPEG specification. pigsqueeze automatically handles splitting large blobs of data across multiple chunks, since the limit per chunk is ~65KB. pigsqueeze\'s method allows for payload sizes of up ot ~15MB per segment. Multiple unused segments are available, so there is a theoretical limit of 135MB per image, which is probably plenty. If you need more, you should probably look at a different solution to your problem.\n\n## Installation\npigsuqeeze can be installed via pip:\n```bash\n$ pip install pigsqueeze\n```\n\n## Usage\n```bash\nUsage: psz write [OPTIONS] INPUT_IMAGE DATA OUTPUT_FILE\n\nOptions:\n  -s, --segment INTEGER  [required]\n  -i, --identifier TEXT  [required]\n  --help                 Show this message and exit.\n```\n\n```bash\nUsage: psz read [OPTIONS] INPUT_IMAGE OUTPUT_FILE\n\nOptions:\n  -s, --segment INTEGER  [required]\n  -i, --identifier TEXT  [required]\n  --help                 Show this message and exit.\n```\n\nAs a Python library:\n```python\nfrom pigsqueeze import Image\n\n# Write some text to App segment 4 with identifier PSZ\nimage = Image("path/to/image.jpg")\nimage.write(4, "PSZ", b"Some bytes to save in the file.")\nimage.save("path/to/output.jpg")\n\n# Retrieve the text from the modified image file\nimage = Image("path/to/output.jpg")\nresult = image.read(4, "PSZ")\n```\n',
    'author': 'Tim Wedde',
    'author_email': 'timwedde@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/timwedde/pigsqueeze',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
