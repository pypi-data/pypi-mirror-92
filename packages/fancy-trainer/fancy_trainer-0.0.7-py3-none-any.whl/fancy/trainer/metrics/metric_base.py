from abc import ABC, abstractmethod

import torch


class MetricBase(ABC):

    @abstractmethod
    def evaluate(self, value: torch.Tensor, target: torch.Tensor) -> float:
        pass

    @abstractmethod
    def get_value(self) -> float:
        pass

    def get_name(self) -> str:
        return type(self).__name__.lower()

    def reset_states(self) -> None:
        pass

    def __str__(self):
        return f'{self.get_name()}={self.get_value():.6f}'

