from typing_extensions import Protocol, runtime_checkable

__all__ = ["Sized"]


@runtime_checkable
class Sized(Protocol):
    def __len__(self) -> int:
        ...
