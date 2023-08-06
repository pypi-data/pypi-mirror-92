# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matching_network']

package_data = \
{'': ['*']}

install_requires = \
['quantiphy>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'matching-network',
    'version': '0.0.5',
    'description': 'Design lumped-parameters matching networks (L-sections)',
    'long_description': '<div align="right" style="text-align:right"><i><a href="https://urbanij.github.io/">Francesco Urbani</a></i></div>\n\n### Index of Jupyter (IPython) Notebooks\n\n|Title                                                                                                           |\n|----------------------------------------------------------------------------------------------------------------|\n|<a href="https://github.com/urbanij/matching-network/blob/master/aux/L-section_matching_calculations.ipynb">L-section_matching_calculations</a>|\n|<a href="https://github.com/urbanij/matching-network/blob/master/aux/calculations.ipynb">Calculations</a>|\n|<a href="https://github.com/urbanij/matching-network/blob/master/aux/demo_matching_network.ipynb">Demo</a>|\n\n\n\n---\n\n\n[![Downloads](https://pepy.tech/badge/matching-network)](https://pepy.tech/project/matching-network)\n\n\nInstallation\n============\n\n```sh\npip install matching-network\n```\n\n\n\nDocumentation\n=============\n\n\n```python\nimport matching_network as mn\n\n\nimpedance_you_have         = 90 + 32j # Ω \nimpedance_you_want_to_have = 175      # Ω\n\nfrequency                  = 900e6    # Hz\n\nmn.L_section_matching(impedance_you_have, impedance_you_want_to_have, frequency).match()\n```\n',
    'author': 'Francesco Urbani',
    'author_email': 'francescourbanidue@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/matching-network/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
