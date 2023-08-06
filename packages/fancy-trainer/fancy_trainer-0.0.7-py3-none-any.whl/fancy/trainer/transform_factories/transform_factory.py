from abc import ABC
from typing import Callable, Optional


class TransformsFactory(ABC):

    @property
    def train_transform(self) -> Optional[Callable]:
        return None

    @property
    def train_target_transform(self) -> Optional[Callable]:
        return None

    @property
    def test_transform(self) -> Optional[Callable]:
        return None

    @property
    def test_target_transform(self) -> Optional[Callable]:
        return None

    @property
    def valid_transform(self) -> Optional[Callable]:
        return None

    @property
    def valid_target_transform(self) -> Optional[Callable]:
        return None
