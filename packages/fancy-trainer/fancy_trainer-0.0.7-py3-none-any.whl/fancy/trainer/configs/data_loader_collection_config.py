from typing import Optional

from cached_property import cached_property

from . import DatasetConfig, TransformConfig
from fancy import config as cfg
from ..training import DataLoaderCollection


class DataLoaderCollectionConfig(cfg.BaseConfig):
    transform: TransformConfig = cfg.Option(required=True, type=TransformConfig)

    train: DatasetConfig = cfg.Option(required=True, type=DatasetConfig)
    test: DatasetConfig = cfg.Option(required=True, type=DatasetConfig)
    valid: Optional[DatasetConfig] = cfg.Option(nullable=True, type=DatasetConfig)

    @cached_property
    def data_loader_collection(self):
        self.train.set_transforms(
            self.transform.transform_factory.train_transform,
            self.transform.transform_factory.train_target_transform
        )
        self.test.set_transforms(
            self.transform.transform_factory.test_transform,
            self.transform.transform_factory.test_target_transform
        )

        if self.valid is not None:
            self.valid.set_transforms(
                self.transform.transform_factory.valid_transform,
                self.transform.transform_factory.valid_target_transform
            )

        return DataLoaderCollection(
            self.train.loader,
            self.test.loader,
            self.valid.loader if self.valid is not None else None
        )
