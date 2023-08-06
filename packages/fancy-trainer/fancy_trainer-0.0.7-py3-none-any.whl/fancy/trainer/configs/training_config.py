from typing import Callable

from cached_property import cached_property
from torch.optim.optimizer import Optimizer

from fancy import config as cfg
from torch.nn import Module

from . import TrainerConfig, ModelConfig, OptimizerConfig, LossFunctionConfig, \
    DataLoaderCollectionConfig, MetricsCollectionConfig
from ..training import DataLoaderCollection, Trainer
from ..training.metrics_collection import MetricsCollection


class TrainingConfig(cfg.BaseConfig):
    profile_name: str = cfg.Option(required=True, type=str)
    _model: ModelConfig = cfg.Option(name="model", required=True, type=ModelConfig)
    _optimizer: OptimizerConfig = cfg.Option(name="optimizer", required=True, type=OptimizerConfig)
    dataset: DataLoaderCollectionConfig = cfg.Option(required=True, type=DataLoaderCollectionConfig)
    metrics: MetricsCollectionConfig = cfg.Option(default={}, type=MetricsCollectionConfig)

    _trainer: TrainerConfig = cfg.Option(name="trainer", required=True, type=TrainerConfig)
    _loss_func: LossFunctionConfig = cfg.Option(name="loss_func", required=True, type=LossFunctionConfig)

    @property
    def model(self) -> Module:
        return self._model.model

    @cached_property
    def optimizer(self) -> Optimizer:
        self._optimizer.set_model(self.model)
        return self._optimizer.optimizer

    @property
    def loss_func(self) -> Callable:
        return self._loss_func.eval_loss

    @property
    def data_loader_collection(self) -> DataLoaderCollection:
        return self.dataset.data_loader_collection

    @property
    def metrics_collection(self) -> MetricsCollection:
        return self.metrics.metrics_collection

    @cached_property
    def trainer(self) -> Trainer:
        return Trainer(
            self._get_out_prefix(),
            self.data_loader_collection,
            self.metrics_collection,
            self.loss_func,
            self.model,
            self.optimizer,
            self._trainer.out,
            self._trainer.train_rate,
            self._trainer.max_epochs,
            self._trainer.save_checkpoint_epochs,
            self._trainer.device,
            self._trainer.half,
            self._trainer.ddp
        )

    def _get_out_prefix(self) -> str:
        cls_name = self._model.imported.__name__
        return self.profile_name + "_" + cls_name
