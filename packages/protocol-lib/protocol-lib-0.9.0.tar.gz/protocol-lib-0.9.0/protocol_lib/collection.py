from typing import TypeVar

from typing_extensions import Protocol, runtime_checkable

from .iterable import Iterator

__all__ = ["Collection"]


T = TypeVar("T")


@runtime_checkable
class Collection(Protocol[T]):
    def __contains__(self, item: T) -> bool:
        ...

    def __iter__(self) -> Iterator[T]:
        ...

    def __len__(self) -> int:
        ...
