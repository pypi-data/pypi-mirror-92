from cached_property import cached_property

from torch.nn import Module
from torch.optim.optimizer import Optimizer

from fancy import config as cfg

from . import ImporterConfig


class OptimizerConfig(ImporterConfig):
    param: dict = cfg.Option(default={}, type=cfg.process.flag_container)
    model: Module = None

    def set_model(self, model: Module) -> None:
        self.model = model

    @cached_property
    def optimizer(self) -> Optimizer:
        if self.model is None:
            raise ValueError("model has not loaded.")

        if not isinstance(self.param, dict):
            raise TypeError("params must be a dict")

        optimizer = self.imported(self.model.parameters(), **self.param)
        if not isinstance(optimizer, Optimizer):
            raise TypeError("imported_cls must be subclass of torch.optim.Optimizer or a Callable returned it.")
        return optimizer
