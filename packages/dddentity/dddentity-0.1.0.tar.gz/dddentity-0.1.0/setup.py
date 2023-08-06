# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dddentity']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dddentity',
    'version': '0.1.0',
    'description': 'DDD entity',
    'long_description': '# dddentity\n\n[![PyPI](https://img.shields.io/pypi/v/dddentity)](https://pypi.org/project/dddentity/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dddentity)](https://pypi.org/project/dddentity/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![license](https://img.shields.io/github/license/nekonoshiri/dddentity)](https://github.com/nekonoshiri/dddentity/blob/main/LICENSE)\n\nDDD entity.\n\n## Usage\n\n```Python\nfrom dddentity import Entity, ref\n\nUserId = str\n\n\nclass User(Entity[UserId]):\n    def __init__(self, id: UserId, name: str) -> None:\n        self.id = id\n        self.name = name\n\n    def _ref_(self) -> UserId:\n        return self.id\n\n\nassert User("0001", "Gilgamesh") == User("0001", "Bilgamesh")\n\nassert ref(User("0002", "Enkidu")) == "0002"\n```\n\n## Caveat\n\nCurrently `eq=False` must be set when using with dataclasses\nto prevent to generate `__eq__()` method by dataclass.\n\n```Python\n@dataclass(eq=False)\nclass User(Entity[UserId]):\n    ...\n```\n\n## API\n\n### Module `dddentity`\n\n#### *abstract class* `Entity[T]`\n\nEntity class.\nClasses implementing this class must implement abstract method `_ref_()`.\n\nThis class is hashable, satisfying the following conditions:\n\n- `entity1 == entity2` iff `entity1._ref_() == entity2._ref_()`\n- `hash(entity) == hash(entity._ref_())`\n\nwhere entity, entity1, entity2 are entities.\n\n##### *type parameter* `T`\n\nType of the identifier of the entity, which must be hashable.\n\n##### *abstract method* `_ref_() -> T`\n\nShall return the identifier of the entity.\n\n#### *function* `ref(entity: Entity[T]) -> T`\n\nReturn `entity._ref_()`.\n',
    'author': 'Shiri Nekono',
    'author_email': 'gexira.halen.toms@gmail.com',
    'maintainer': 'Shiri Nekono',
    'maintainer_email': 'gexira.halen.toms@gmail.com',
    'url': 'https://github.com/nekonoshiri/dddentity',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
