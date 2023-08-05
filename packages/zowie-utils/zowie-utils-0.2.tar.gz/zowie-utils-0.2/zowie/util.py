from typing import TypeVar, Sequence, Optional

T = TypeVar("T")


def head_option(ls: Sequence[T]) -> Optional[T]:
    return ls[0] if ls else None
