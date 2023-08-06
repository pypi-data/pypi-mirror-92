from abc import ABC, abstractmethod
from matplotlib import pyplot as plt

from . import Checkpoint


class CheckpointPlotterBase(ABC):

    @abstractmethod
    def plot(self, checkpoint: Checkpoint) -> plt.Figure:
        pass
