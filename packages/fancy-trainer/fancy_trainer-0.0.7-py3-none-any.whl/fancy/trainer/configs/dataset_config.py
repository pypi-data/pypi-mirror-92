from typing import MutableMapping, Callable

from ..configs import ImporterConfig
from fancy import config as cfg
from torch.utils.data import DataLoader, Dataset


class DatasetConfig(ImporterConfig):
    param: dict = cfg.Option(default={}, type=cfg.process.flag_container)

    batch_size: int = cfg.Option(default=1, type=int)
    shuffle: bool = cfg.Option(default=False, type=bool)
    pin_memory: bool = cfg.Option(default=True, type=bool)
    num_workers: int = cfg.Option(default=0, type=int)
    transform: Callable = None
    target_transform: Callable = None

    def set_transforms(self, transform: Callable, target_transform: Callable):
        self.transform = transform
        self.target_transform = target_transform

    @property
    def loader(self) -> DataLoader:
        loader = DataLoader(
            self.dataset,
            shuffle=self.shuffle,
            pin_memory=self.pin_memory,
            batch_size=self.batch_size,
            num_workers=self.num_workers
        )

        return loader

    # TODO transform and target_transform
    @property
    def dataset(self) -> Dataset:
        cls = self.imported
        if not isinstance(cls, type):
            raise ValueError("Dataset type should be a class name.")
        if not issubclass(cls, Dataset):
            raise ValueError(f"Incorrect dataset type: {cls}.")
        if not isinstance(self.param, MutableMapping):
            raise ValueError('param must be instance of MutableMapping')
        dataset = cls(transform=self.transform, target_transform=self.target_transform, **self.param)

        return dataset
