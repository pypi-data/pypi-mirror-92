from typing import TypeVar, Generic, Optional

T = TypeVar("T")


class TargetHandler(Generic[T]):
    target = None

    def set(self, target: T) -> None:
        self.target = target

    def get(self, default: T = None) -> Optional[T]:
        return self.target if self.target is not None else default

    def clear(self) -> None:
        self.target = None

    def __call__(self, default: T) -> T:
        return self.get(default)
