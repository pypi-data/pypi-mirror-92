import torch

from ..metrics import MetricBase


class RMSE(MetricBase):
    count: int
    accumulated_loss: float

    mse_loss_fn = torch.nn.MSELoss()

    def reset_states(self) -> None:
        self.count = 0
        self.accumulated_loss = 0.

    def evaluate(self, value: torch.Tensor, target: torch.Tensor) -> float:
        item = torch.sqrt(self.mse_loss_fn(value, target)).item()
        self.count += value.size(0)
        self.accumulated_loss += item
        return item / value.size(0)

    def get_value(self) -> float:
        return self.accumulated_loss / self.count
