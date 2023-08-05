from typing import TypeVar, Union, overload

from typing_extensions import Protocol, runtime_checkable

from .iterable import Iterable, Iterator

__all__ = [
    "Sequence",
    "MutableSequence",
]


T = TypeVar("T")


@runtime_checkable
class Sequence(Protocol[T]):
    def __contains__(self, item: T) -> bool:
        ...

    def __iter__(self) -> Iterator[T]:
        ...

    def __reversed__(self) -> Iterator[T]:
        ...

    def __len__(self) -> int:
        ...

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> "Sequence[T]":
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[T, "Sequence[T]"]:
        ...

    def index(self, value: T, start: int = ..., stop: int = ...) -> int:
        ...

    def count(self, value: T) -> int:
        ...


@runtime_checkable
class MutableSequence(Protocol[T]):
    def __contains__(self, item: T) -> bool:
        ...

    def __iter__(self) -> Iterator[T]:
        ...

    def __reversed__(self) -> Iterator[T]:
        ...

    def __len__(self) -> int:
        ...

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> "MutableSequence[T]":
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[T, "MutableSequence[T]"]:
        ...

    def index(self, value: T, start: int = ..., stop: int = ...) -> int:
        ...

    def count(self, value: T) -> int:
        ...

    def __setitem__(self, index: int, value: T) -> None:
        ...

    def __delitem__(self, index: int) -> None:
        ...

    def insert(self, index: int, value: T) -> None:
        ...

    def append(self, value: T) -> None:
        ...

    def clear(self) -> None:
        ...

    def reverse(self) -> None:
        ...

    def extend(self, values: Sequence[T]) -> None:
        ...

    def pop(self, index: int = ...) -> T:
        ...

    def remove(self, value: T) -> None:
        ...

    def __iadd__(self, values: Iterable[T]) -> "MutableSequence[T]":
        ...
