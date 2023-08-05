# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['veils']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=4.2.0,<5.0.0', 'wrapt>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'veils',
    'version': '0.2.1',
    'description': 'Python Veil Objects',
    'long_description': '# Veils\n[![EO principles respected here](https://www.elegantobjects.org/badge.svg)](https://www.elegantobjects.org)\n[![Build Status](https://travis-ci.org/monomonedula/veils.svg?branch=main)](https://travis-ci.org/monomonedula/veils)\n[![codecov](https://codecov.io/gh/monomonedula/veil/branch/main/graph/badge.svg)](https://codecov.io/gh/monomonedula/veil)\n[![PyPI version](https://badge.fury.io/py/veils.svg)](https://badge.fury.io/py/veils)\n\n`veils` is a python implementation of a ruby [veils package](https://github.com/yegor256/veils).\nLong story short, it provides convenient object decorators for data memoization.\n\n\n\n## Installation\n\n`pip install veils`\n\n## Usage\n\n```python\nfrom veils import veil\n\nobj = veil(\n    obj,\n    methods={"__str__": "hello, world!", "foo": "42"}\n)\nstr(obj)  # returns "hello, world!"\nobj.foo()  # returns "42"\n```\n\nThe methods `__str__` and `foo` will return "Hello, world!" and "42" respectively\nuntil some other method is called and the veil is "pierced".\n\nYou can also use `unpiercable` decorator, which will never be pierced: a very good instrument for data memoization.\n\nAnd it works the same way for asynchronous methods too\n\n```python\nobj = veil(\n    obj,\n    async_methods={"foo": "42"}\n)\nawait obj.foo()     # returns "42"\n```\n\nAnd also for properties\n```python\nobj = veil(\n    obj,\n    props={"bar": "42"}\n)\n\nobj.bar     # equals "42"\n```\n\nThis library also extends the original one with a caching decorator `memo`. Use it like this:\n```python\nfrom veils import memo\n\nobj = memo(\n    obj,\n    cacheable={"foo", "bar", "baz", "__str__"} \n    # \'cacheable\' is a collection of methods (both regular and asynchronous) \n    # and properties to be cached\n)\n```\n\n## Advanced usage\n\nThe python implementations of veil is somewhat tricky due to the magic methods which\nare being accessed bypassing the `__getattribute__` method.\nTherefore, this implementation, in this particular case, relies on metaclasses in order to define magic methods on the fly in the veil object so that they correspond to those defined in the object being wrapped.\n\n`veil` and `unpiercable` are just shortcuts to `VeilFactory(Veil).veil_of` and `VeilFactory(Unpiercable).veil_of`.\n\nIn some advanced cases you may want a different list of magic methods to be transparent or proxied by a veil object. In oder to obtain such behavior\nyou may create a custom veil factory like so: `VeilFactory(Veil, proxied_dunders, naked_dunders)`. \n`naked_dunders` is a list of methods bypassing the veil.\n`proxied_dunders` is a list of methods to be veiled.\n',
    'author': 'monomonedula',
    'author_email': 'valh@tuta.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/monomonedula/veil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
