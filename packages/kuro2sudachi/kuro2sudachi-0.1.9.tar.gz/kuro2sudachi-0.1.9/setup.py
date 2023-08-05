# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kuro2sudachi']

package_data = \
{'': ['*']}

install_requires = \
['jaconv>=0.2.4,<0.3.0']

entry_points = \
{'console_scripts': ['kuro2sudachi = kuro2sudachi.core:cli']}

setup_kwargs = {
    'name': 'kuro2sudachi',
    'version': '0.1.9',
    'description': '',
    'long_description': '# kuro2sudachi\n\n[![PyPi version](https://img.shields.io/pypi/v/kuro2sudachi.svg)](https://pypi.python.org/pypi/kuro2sudachi/)\n![PyTest](https://github.com/po3rin/kuro2sudachi/workflows/PyTest/badge.svg)\n[![](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)\n\nkuro2sudachi lets you to convert kuromoji user dict to sudachi user dict.\n\n# Usage\n\n```sh\n$ pip install kuro2sudachi\n\n# prepase riwirte.def\n# https://github.com/WorksApplications/Sudachi/blob/develop/src/main/resources/rewrite.def\n$ ls\nrewiite.def\n\n$ kuro2sudachi kuromoji_dict.txt -o sudachi_user_dict.txt\n```\n\n# Develop\n\ntest kuro2sudachi\n\n```sh\n$ poetry install\n$ poetry run pytest\n```\n\nexec kuro2sudachi command\n\n```sh\n$ poetry run kuro2sudachi tests/kuromoji_dict_test.txt -o sudachi_user_dict.txt\n```\n\n## Supported pos\n\n```sh\n* 固有名詞 -> 名詞,固有名詞,一般,*,*,*\n* 名詞 -> 名詞,普通名詞,一般,*,*,*\n* 記号 -> 記号,一般,*,*,*,*\n* 形容詞 -> 形容詞,一般,*,*,*,*\n* 副詞 -> 副詞,*,*,*,*,*\n* 動詞 -> 動詞,一般,*,*,*,*\n```\n\nif you want to ignore unsupported pos error, use `--ignore` flag.\n\n## TODO\n\n- [ ] split mode\n- [ ] change connection cost\n- [ ] supports many pos\n- [ ] supports custom dict converts pos\n\n',
    'author': 'po3rin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/po3rin/kuro2sudachi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
