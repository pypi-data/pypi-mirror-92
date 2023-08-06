from copy import deepcopy
from typing import List, Dict, TYPE_CHECKING

from torch.nn import Module
from torch.nn.parallel import DistributedDataParallel

from torch.optim.optimizer import Optimizer

from ..metrics import MetricBase

if TYPE_CHECKING:
    from ..training.metrics_collection import MetricsCollection


class Checkpoint:
    model_state: dict
    optimizer_state: dict

    epoch: int
    indicate: float

    train_metrics: Dict[str, List[float]]
    test_metrics: Dict[str, List[float]]
    valid_metrics: Dict[str, List[float]]

    def __init__(self):
        self.train_metrics = {}
        self.test_metrics = {}
        self.valid_metrics = {}

    def add_metrics(self, metrics: "MetricsCollection"):
        self._add_metrics_to_specific_dict(metrics.train_metrics, self.train_metrics)
        self._add_metrics_to_specific_dict(metrics.test_metrics, self.test_metrics)
        self._add_metrics_to_specific_dict(
            metrics.valid_metrics if metrics.valid_metrics is not None else [],
            self.test_metrics
        )

    def _add_metrics_to_specific_dict(self, metrics: List[MetricBase], metrics_dict: dict):
        for metric in metrics:
            name = metric.get_name()
            if name not in metrics_dict.keys():
                metrics_dict[name] = []
            metrics_dict[name].append(metric.get_value())

    def set_states(self, model: Module, optimizer: Optimizer):
        self.model_state = (model.module if isinstance(model, DistributedDataParallel) else model).state_dict()
        self.optimizer_state = optimizer.state_dict()

    def set_epoch(self, epoch: int):
        self.epoch = epoch

    def set_indicate(self, indicate: float):
        self.indicate = indicate

    def copy(self) -> "Checkpoint":
        return deepcopy(self)

    def state_dict(self) -> dict:
        return vars(self.copy())

    def load(self, state_dict: dict) -> None:
        for k, v in state_dict.items():
            setattr(self, k, v)
