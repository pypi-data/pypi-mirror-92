from pathlib import Path

import torch
from fancy import config as cfg

from .processes import DEVICE_AUTO, process_device


class TrainerConfig(cfg.BaseConfig):
    out: Path = cfg.Option(required=True, type=Path)
    train_rate: float = cfg.Option(default=0.1, type=float)

    max_epochs: int = cfg.Option(required=True, type=int)
    save_checkpoint_epochs: int = cfg.Option(default=20, type=int)

    device: torch.device = cfg.Option(default=DEVICE_AUTO, type=process_device)
    half: bool = cfg.Option(default=True, type=bool)
    ddp: bool = cfg.Option(default=True, type=bool)
    test_no_grad: bool = cfg.Option(default=True, type=bool)

    # TODO callback

    def post_load(self):
        self.half = self.half and self._is_half_available()
        self.ddp = self.ddp and torch.cuda.is_available() and "cuda" in self.device.type

    def _is_half_available(self):
        try:
            import apex
            return torch.cuda.is_available()
        except ImportError as _:
            return False
