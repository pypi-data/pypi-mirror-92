from cached_property import cached_property

from . import ImporterConfig
from ..transform_factories import TransformsFactory
from fancy import config as cfg


class TransformConfig(ImporterConfig):
    param: dict = cfg.Option(default={}, type=cfg.process.flag_container)

    @cached_property
    def transform_factory(self) -> TransformsFactory:
        if issubclass(self.imported, TransformsFactory):
            return self.imported(**self.param)
        raise TypeError("imported must be TransformFactory")
