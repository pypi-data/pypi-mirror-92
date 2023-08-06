# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vak',
 'vak.cli',
 'vak.config',
 'vak.core',
 'vak.datasets',
 'vak.engine',
 'vak.files',
 'vak.io',
 'vak.metrics',
 'vak.metrics.classification',
 'vak.metrics.distance',
 'vak.models',
 'vak.plot',
 'vak.split',
 'vak.split.algorithms',
 'vak.transforms']

package_data = \
{'': ['*']}

install_requires = \
['SoundFile>=0.10.3,<0.11.0',
 'attrs>=20.3.0,<21.0.0',
 'crowsetta>=3.1.0',
 'dask[bag]>=2021.1.0,<2022.0.0',
 'evfuncs>=0.3.1,<0.4.0',
 'joblib>=1.0.0,<2.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'numpy>=1.19.4,<2.0.0',
 'pandas>=1.1.5,<2.0.0',
 'scipy>=1.5.4,<2.0.0',
 'tensorboard>=2.2.0,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'torch>=1.7.1,<2.0.0',
 'torchvision>=0.8.2,<0.9.0',
 'tqdm>=4.55.0,<5.0.0']

entry_points = \
{'console_scripts': ['vak = vak.__main__:main'],
 'vak.metrics': ['Accuracy = vak.metrics.Accuracy',
                 'Levenshtein = vak.metrics.Levenshtein',
                 'SegmentErrorRate = vak.metrics.SegmentErrorRate']}

setup_kwargs = {
    'name': 'vak',
    'version': '0.4.0.dev1',
    'description': 'neural network toolbox for animal communication and bioacoustics',
    'long_description': None,
    'author': 'David Nicholson',
    'author_email': 'nickledave@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
