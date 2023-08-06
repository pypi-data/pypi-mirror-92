from typing import Callable, Optional

import torch

from ..metrics import MetricBase


class Loss(MetricBase):
    loss_fn: Callable
    count: int
    accumulated_loss: float

    _eval_cache: Optional[torch.Tensor]

    def __init__(self, loss_fn: Callable):
        self.loss_fn = loss_fn

    def evaluate(self, value: torch.Tensor, target: torch.Tensor) -> float:
        self._eval_cache = self.loss_fn(value, target)
        self.count += value.size(0)
        item = self._eval_cache.item()
        self.accumulated_loss += item
        return item / value.size(0)

    def get_value(self) -> float:
        return self.accumulated_loss / self.count

    def reset_states(self) -> None:
        self.count = 0
        self.accumulated_loss = 0
        self._eval_cache = None

    def get_tensor(self) -> torch.Tensor:
        return self._eval_cache
