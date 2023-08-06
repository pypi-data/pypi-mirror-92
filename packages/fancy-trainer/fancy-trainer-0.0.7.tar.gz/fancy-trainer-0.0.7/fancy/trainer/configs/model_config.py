from cached_property import cached_property
from torch.nn import Module
from fancy import config as cfg

from . import ImporterConfig


class ModelConfig(ImporterConfig):
    param: dict = cfg.Option(default={}, type=cfg.process.flag_container)

    @cached_property
    def model(self) -> Module:
        if not isinstance(self.param, dict):
            raise TypeError("params must be a dict")
        model = self.imported(**self.param)

        if not isinstance(model, Module):
            raise TypeError("imported_cls must be subclass of torch.nn.Module or a Callable returned it.")

        return model
