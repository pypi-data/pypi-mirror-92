# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['deepqmc',
 'deepqmc.data',
 'deepqmc.extra',
 'deepqmc.torchext',
 'deepqmc.wf',
 'deepqmc.wf.paulinet']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.16,<2.0',
 'toml>=0.10.0,<0.11.0',
 'torch>=1.2,<2.0',
 'uncertainties>=3.1.2,<4.0.0']

extras_require = \
{'all': ['scipy>=1.2,<2.0',
         'pyscf>=1.6,<2.0',
         'pytest>=5,<7',
         'coverage>=4.5,<6',
         'tensorboard>=2.0,<3.0',
         'tqdm>=4.31,<5.0',
         'h5py>=2.10.0,<4',
         'Pillow>=7,<9',
         'click>=7.0,<8.0',
         'tomlkit>=0.7.0,<0.8.0'],
 'cli': ['click>=7.0,<8.0', 'tomlkit>=0.7.0,<0.8.0'],
 'doc': ['sphinx>=2.2,<3.0', 'sphinxcontrib-katex>=0.5.1,<0.6.0'],
 'test': ['pytest>=5,<7', 'coverage>=4.5,<6'],
 'train': ['tensorboard>=2.0,<3.0',
           'tqdm>=4.31,<5.0',
           'h5py>=2.10.0,<4',
           'Pillow>=7,<9'],
 'wf': ['scipy>=1.2,<2.0', 'pyscf>=1.6,<2.0']}

entry_points = \
{'console_scripts': ['deepqmc = deepqmc.cli:cli']}

setup_kwargs = {
    'name': 'deepqmc',
    'version': '0.3.0',
    'description': 'Deep-learning quantum Monte Carlo for electrons in real space',
    'long_description': "# DeepQMC\n\n[![build](https://img.shields.io/travis/com/deepqmc/deepqmc/master.svg)](https://travis-ci.com/deepqmc/deepqmc)\n[![coverage](https://img.shields.io/codecov/c/github/deepqmc/deepqmc.svg)](https://codecov.io/gh/deepqmc/deepqmc)\n![python](https://img.shields.io/pypi/pyversions/deepqmc.svg)\n[![pypi](https://img.shields.io/pypi/v/deepqmc.svg)](https://pypi.org/project/deepqmc/)\n[![commits since](https://img.shields.io/github/commits-since/deepqmc/deepqmc/latest.svg)](https://github.com/deepqmc/deepqmc/releases)\n[![last commit](https://img.shields.io/github/last-commit/deepqmc/deepqmc.svg)](https://github.com/deepqmc/deepqmc/commits/master)\n[![license](https://img.shields.io/github/license/deepqmc/deepqmc.svg)](https://github.com/deepqmc/deepqmc/blob/master/LICENSE)\n[![code style](https://img.shields.io/badge/code%20style-black-202020.svg)](https://github.com/ambv/black)\n[![chat](https://img.shields.io/gitter/room/deepqmc/deepqmc)](https://gitter.im/deepqmc/deepqmc)\n[![doi](https://img.shields.io/badge/doi-10.5281%2Fzenodo.3960826-blue)](http://doi.org/10.5281/zenodo.3960826)\n\nDeepQMC implements variational quantum Monte Carlo for electrons in molecules, using deep neural networks written in [PyTorch](https://pytorch.org) as trial wave functions. Besides the core functionality, it contains implementations of the following ansatzes:\n\n- PauliNet: https://doi.org/10.1038/s41557-020-0544-y\n\n## Installing\n\nInstall and update using [Pip](https://pip.pypa.io/en/stable/quickstart/).\n\n```\npip install -U deepqmc[wf,train,cli]\n```\n\n## A simple example\n\n```python\nfrom deepqmc import Molecule, evaluate, train\nfrom deepqmc.wf import PauliNet\n\nmol = Molecule.from_name('LiH')\nnet = PauliNet.from_hf(mol).cuda()\ntrain(net)\nevaluate(net)\n```\n\nOr on the command line:\n\n```\n$ cat lih/param.toml\nsystem = 'LiH'\nansatz = 'paulinet'\n[train_kwargs]\nn_steps = 40\n$ deepqmc train lih --save-every 20\nconverged SCF energy = -7.9846409186467\nequilibrating: 49it [00:07,  6.62it/s]\ntraining: 100%|███████| 40/40 [01:30<00:00,  2.27s/it, E=-8.0302(29)]\n$ ln -s chkpts/state-00040.pt lih/state.pt\n$ deepqmc evaluate lih\nevaluating:  24%|▋  | 136/565 [01:12<03:40,  1.65it/s, E=-8.0396(17)]\n```\n\n## Links\n\n- Documentation: https://deepqmc.github.io\n",
    'author': 'Jan Hermann',
    'author_email': 'jan.hermann@fu-berlin.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/deepqmc/deepqmc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
