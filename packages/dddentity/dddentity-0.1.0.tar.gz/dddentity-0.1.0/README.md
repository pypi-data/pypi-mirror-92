# dddentity

[![PyPI](https://img.shields.io/pypi/v/dddentity)](https://pypi.org/project/dddentity/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dddentity)](https://pypi.org/project/dddentity/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![license](https://img.shields.io/github/license/nekonoshiri/dddentity)](https://github.com/nekonoshiri/dddentity/blob/main/LICENSE)

DDD entity.

## Usage

```Python
from dddentity import Entity, ref

UserId = str


class User(Entity[UserId]):
    def __init__(self, id: UserId, name: str) -> None:
        self.id = id
        self.name = name

    def _ref_(self) -> UserId:
        return self.id


assert User("0001", "Gilgamesh") == User("0001", "Bilgamesh")

assert ref(User("0002", "Enkidu")) == "0002"
```

## Caveat

Currently `eq=False` must be set when using with dataclasses
to prevent to generate `__eq__()` method by dataclass.

```Python
@dataclass(eq=False)
class User(Entity[UserId]):
    ...
```

## API

### Module `dddentity`

#### *abstract class* `Entity[T]`

Entity class.
Classes implementing this class must implement abstract method `_ref_()`.

This class is hashable, satisfying the following conditions:

- `entity1 == entity2` iff `entity1._ref_() == entity2._ref_()`
- `hash(entity) == hash(entity._ref_())`

where entity, entity1, entity2 are entities.

##### *type parameter* `T`

Type of the identifier of the entity, which must be hashable.

##### *abstract method* `_ref_() -> T`

Shall return the identifier of the entity.

#### *function* `ref(entity: Entity[T]) -> T`

Return `entity._ref_()`.
