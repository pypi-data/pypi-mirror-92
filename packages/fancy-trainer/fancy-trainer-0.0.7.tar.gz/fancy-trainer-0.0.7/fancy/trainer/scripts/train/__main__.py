import argparse
from pathlib import Path

import torch

from fancy.trainer.model import CheckpointPlotter
from fancy import config as cfg

from matplotlib import pyplot as plt
from fancy.trainer.configs import TrainingConfig


def main():
    args = get_argparser().parse_args()
    config = TrainingConfig(cfg.YamlConfigLoader(args.config_path))
    print(config)
    if args.checkpoint is not None:
        config.trainer.load_checkpoint(torch.load(args.checkpoint, map_location="cpu"))
    config.trainer.train()

    last_checkpoint = config.trainer.checkpoint
    best_checkpoint = config.trainer.best_checkpoint

    plotter = CheckpointPlotter()

    fig_data_list = [
        ('last', last_checkpoint),
        ('best', best_checkpoint)
    ]

    for checkpoint_name, checkpoint in fig_data_list:
        figs = plotter.plot(checkpoint)
        for metric_name, fig in figs.items():
            filename = f'{config.trainer.out_prefix}_{checkpoint_name}_{metric_name}'
            fig.suptitle(filename.replace("_", " "))
            fig.savefig(config.trainer.out / f"{filename}.png")
            fig.show()
            plt.close(fig)


def get_argparser():
    parser = argparse.ArgumentParser()
    path = lambda x: Path(x)
    parser.add_argument("config_path", type=path, help="path to config file")
    parser.add_argument("-c", "--checkpoint", type=path, help="the checkpoint will be loaded")
    return parser


if __name__ == '__main__':
    main()
