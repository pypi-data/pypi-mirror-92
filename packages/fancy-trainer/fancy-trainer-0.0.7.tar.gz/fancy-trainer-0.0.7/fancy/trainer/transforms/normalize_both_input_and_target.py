from typing import Optional, Callable

import torch
import numpy as np
from PIL.Image import Image

from ..transforms import TargetHandler


class NormalizeBothInputAndTarget:
    transform: Callable[[Image], Image]
    target_handler: TargetHandler

    def __init__(
            self,
            transform: Callable[[Image], Image],
            target_handler: Optional[TargetHandler] = None,
    ):
        self.target_handler = target_handler
        self.transform = transform

    def forward(self, x: Image) -> torch.Tensor:
        image_data = np.array(x)
        std = image_data.std()
        mean = image_data.mean()
        erased_img = self.transform(x)
        erased_img_data = torch.tensor(np.array(erased_img), dtype=torch.float32)
        normed_img_data = (erased_img_data - mean) / std
        target = self.target_handler.get()
        if target is None:
            raise RuntimeError("target has not generated.")
        if not isinstance(target, Image):
            raise TypeError("the generated target must be an PIL.Image")
        target_data = torch.tensor(np.array(target), dtype=torch.float32)
        self.target_handler.set((target_data - mean) / std)
        return normed_img_data
