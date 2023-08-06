from typing import List, Type

from cached_property import cached_property

from fancy import config as cfg
from .. import metrics
from ..metrics import MetricBase
from ..training.metrics_collection import MetricsCollection

NOT_FOUND = object()


class MetricsCollectionConfig(cfg.BaseConfig):
    _train: List[str] = cfg.Option(name="train", default=[], type=cfg.config_list(str))
    _test: List[str] = cfg.Option(name="test", default=[], type=cfg.config_list(str))
    _valid: List[str] = cfg.Option(name="valid", default=[], type=cfg.config_list(str))

    @cached_property
    def metrics_collection(self):
        return MetricsCollection(
            self._get_metric_list(self._train),
            self._get_metric_list(self._test),
            self._get_metric_list(self._valid)
        )

    def _get_metric_list(self, metric_names: List[str]) -> List[MetricBase]:
        return [self._get_metric_cls(metric_name)() for metric_name in metric_names]

    def _get_metric_cls(self, metric_name: str) -> Type[MetricBase]:
        cls = vars(metrics).get(metric_name, NOT_FOUND)

        if cls is NOT_FOUND:
            raise KeyError(f"the class {metric_name} was not found.")
        return cls
