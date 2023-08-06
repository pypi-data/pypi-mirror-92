# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['__init__']
install_requires = \
['numpy>=1.17.0,<2.0.0']

setup_kwargs = {
    'name': 'polyagamma',
    'version': '1.0.0b1',
    'description': "Efficiently sample from the Polya-Gamma distribution using NumPy's Generator interface",
    'long_description': '# polya-gamma\nEfficiently sample from the Polya-Gamma distribution using NumPy\'s Generator interface.\n![densities](./scripts/densities.svg)\n\nAs expected, the `saddle` method improves as `h` tends to `infinity`.\n\n## Features\n- `polyagamma` is written in C and optimized for performance.\n- It is flexible and allows the user to sample using one of 4 available methods.\n- Input parameters can be scalars, arrays or both; allowing for easy generation\nof multi-dimensional samples without specifying the size.\n- Random number generation is thread safe.\n- The functional API resembles that of common numpy/scipy functions, therefore making it easy to plugin to\nexisting libraries.\n\n\n## Dependencies\n- Numpy >= 1.17 \n\n\n## Installation\n```shell\n$ pip install -U polyagamma\n```\n\n\n## Example\n\n### Python\n\n```python\nimport numpy as np\nfrom polyagamma import polyagamma\n\no = polyagamma()\n\n# Get a 5 by 10 array of PG(1, 2) variates.\no = polyagamma(z=2, size=(5, 10))\n\n# Pass sequences as input. Numpy\'s broadcasting rules apply here.\nh = [[1, 2, 3, 4, 5], [9, 8, 7, 6, 5]]\no = polyagamma(h, 1)\n\n# Pass an output array\nout = np.empty(5)\npolyagamma(out=out)\nprint(out)\n\n# one can choose a sampling method from {devroye, alternate, gamma, saddle}.\n# If not given, the default behaviour is a hybrid sampler that picks a method\n# based on the parameter values.\no = polyagamma(method="devroye")\n\n# We can also use an existing instance of `numpy.random.Generator` as a parameter.\n# This is useful to reproduce samples generated via a given seed.\nrng = np.random.default_rng(12345)\no = polyagamma(random_state=rng)\n```\n### C\nFor an example of how to use `polyagamma` in a C program, see [here][1].\n\n\n## References\n- Luc Devroye. "On exact simulation algorithms for some distributions related to Jacobi theta functions." Statistics & Probability Letters, Volume 79, Issue 21, (2009): 2251-2259.\n- Polson, Nicholas G., James G. Scott, and Jesse Windle. "Bayesian inference for logistic models using Pólya–Gamma latent variables." Journal of the American statistical Association 108.504 (2013): 1339-1349.\n- J. Windle, N. G. Polson, and J. G. Scott. "Improved Polya-gamma sampling". Technical Report, University of Texas at Austin, 2013b.\n- Windle, Jesse, Nicholas G. Polson, and James G. Scott. "Sampling Polya-Gamma random variates: alternate and approximate techniques." arXiv preprint arXiv:1405.0506 (2014)\n\n\n[1]: ./examples/c_polyagamma.c\n',
    'author': 'Zolisa Bleki',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zoj613/polya-gamma/',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
