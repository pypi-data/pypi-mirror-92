from typing import TypeVar

import torch

DEVICE_AUTO = "==device_auto=="
T = TypeVar("T", dict, list)


def process_device(device_name: str) -> torch.device:
    if device_name == DEVICE_AUTO:
        device_name = "cuda" if torch.cuda.is_available() else "cpu"
    elif not torch.cuda.is_available():  # use cpu when cuda is not available
        device_name = "cpu"
    return torch.device(device_name)
