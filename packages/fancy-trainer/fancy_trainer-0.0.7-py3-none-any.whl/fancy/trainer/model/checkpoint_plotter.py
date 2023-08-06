from typing import Dict

from matplotlib import pyplot as plt

from . import CheckpointPlotterBase, Checkpoint


class CheckpointPlotter(CheckpointPlotterBase):
    def plot(self, checkpoint: Checkpoint) -> Dict[str, plt.Figure]:
        test_plotted = []
        figs = {}
        for name, metric_list in checkpoint.train_metrics.items():
            fig: plt.Figure = plt.figure()
            plt.plot(metric_list, label=f"train {name}")
            if name in checkpoint.test_metrics.keys():
                plt.plot(checkpoint.test_metrics[name], label=f"test {name}")
                test_plotted.append(name)
            plt.legend()
            figs[name] = fig

        for name, metric_list in checkpoint.test_metrics.items():
            if name in test_plotted:
                continue
            fig: plt.Figure = plt.figure()
            plt.plot(metric_list, label=f"test {name}")
            plt.legend()
            figs[name] = fig

        return figs
