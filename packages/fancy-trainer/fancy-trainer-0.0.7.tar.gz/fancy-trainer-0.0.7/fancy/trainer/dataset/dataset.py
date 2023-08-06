from abc import ABC, abstractmethod
from typing import Callable

import torch.utils.data.dataset as dataset


class DatasetBase(dataset.Dataset, ABC):
    transform: Callable
    target_transform: Callable

    def __init__(
            self,
            transform: Callable = None,
            target_transform: Callable = None
    ):
        self.transform = transform
        self.target_transform = target_transform

    @abstractmethod
    def get_data(self, index: int) -> tuple:
        pass

    def __getitem__(self, item: int) -> tuple:
        data, target = self.get_data(item)
        if self.transform is not None:
            data = self.transform(data)

        if self.target_transform is not None:
            target = self.target_transform(target)

        return data, target

    @abstractmethod
    def __len__(self) -> int:
        pass
