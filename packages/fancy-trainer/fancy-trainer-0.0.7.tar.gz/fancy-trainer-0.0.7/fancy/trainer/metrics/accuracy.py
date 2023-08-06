import torch

from ..metrics import MetricBase


class Accuracy(MetricBase):
    correct: int
    total: int

    def evaluate(self, value: torch.Tensor, target: torch.Tensor) -> float:
        self.correct += torch.sum(torch.eq(value.argmax(dim=1), target)).item()
        self.total += value.size(0)
        return self.get_value()

    def get_value(self) -> float:
        return self.correct / self.total

    def reset_states(self) -> None:
        self.correct = 0
        self.total = 0
