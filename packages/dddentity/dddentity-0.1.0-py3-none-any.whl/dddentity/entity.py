from abc import ABC, abstractmethod
from typing import Generic, Hashable, TypeVar

T = TypeVar("T", bound=Hashable)


class Entity(ABC, Generic[T], Hashable):
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        return bool(self._ref_() == other._ref_())

    def __hash__(self) -> int:
        return hash(self._ref_())

    @abstractmethod
    def _ref_(self) -> T:
        ...


def ref(entity: Entity[T]) -> T:
    return entity._ref_()
