from copy import deepcopy
from math import inf
from pathlib import Path
from typing import Callable, List, Dict

import torch
from torch.nn import Module
from torch.nn.parallel import DistributedDataParallel
import torch.distributed as dist

from torch.optim.optimizer import Optimizer
from torch.utils.data import DataLoader

from ..metrics import Loss, MetricBase
from ..model import Checkpoint
from ..training import DataLoaderCollection
from ..training.metrics_collection import MetricsCollection


class Trainer:
    out: Path
    out_prefix: str
    data_loaders: DataLoaderCollection
    metrics: MetricsCollection
    train_rate: float = 0.1

    max_epochs: int
    start_epoch: int
    save_checkpoint_epochs: int

    loss_metric: Loss
    optimizer: Optimizer
    model: Module
    device: torch.device
    half: bool
    ddp: bool
    test_no_grad: bool

    checkpoint: Checkpoint
    best_checkpoint: Checkpoint

    _training_model: Module
    _training_optimizer: Optimizer

    def __init__(
            self,
            out_prefix: str,
            data_loaders: DataLoaderCollection,
            metrics: MetricsCollection,
            loss_function: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
            model: Module,
            optimizer: Optimizer,
            out: Path,
            train_rate: float,
            max_epochs: int,
            save_checkpoint_epochs: int,
            device: torch.device,
            half: bool,
            ddp: bool,
            test_no_grad: bool = True
    ):
        self.out_prefix = out_prefix
        self.data_loaders = data_loaders
        self.metrics = deepcopy(metrics)
        self.loss_metric = Loss(loss_function)

        self.metrics.train_metrics.insert(0, self.loss_metric)
        self.metrics.test_metrics.insert(0, Loss(loss_function))  # test loss metric should calculate independently.

        self.model = model
        self.optimizer = optimizer

        self.out = out
        self.train_rate = train_rate
        self.max_epochs = max_epochs
        self.save_checkpoint_epochs = save_checkpoint_epochs
        self.device = device
        self.half = half
        self.ddp = ddp
        self.test_no_grad = test_no_grad
        self.start_epoch = 0

        self.checkpoint = Checkpoint()
        self.best_checkpoint = Checkpoint()
        self.best_checkpoint.indicate = inf

        self._training_model = self.model
        self._training_optimizer = self.optimizer
        self.setup_training_model_and_optimizer()

    def train(self):
        self.out.mkdir(parents=True, exist_ok=True)

        for epoch in range(self.start_epoch, self.max_epochs):
            self.checkpoint.set_epoch(epoch)
            self.train_epoch(epoch)
            self.test(self.test_no_grad)

            torch.cuda.empty_cache()

            self.checkpoint.add_metrics(self.metrics)
            self.checkpoint.set_indicate(self.calc_indicate(self.train_rate))

            if self.checkpoint.indicate <= self.best_checkpoint.indicate:
                self.checkpoint.set_states(self.model, self.optimizer)
                self.best_checkpoint = self.checkpoint.copy()
                self.save_model(self.out / f'{self.out_prefix}_backup_best.pt', self.best_checkpoint)

            if (epoch + 1) % self.save_checkpoint_epochs == 0:
                self.checkpoint.set_states(self.model, self.optimizer)
                self.save_model(self.out / f'{self.out_prefix}_backup_{epoch + 1}.pt', self.checkpoint)
            print(
                f"\r"
                f"epoch {epoch + 1}/{self.max_epochs} / "
                f"train({', '.join([str(metric) for metric in self.metrics.train_metrics])}) / "
                f"test({', '.join([str(metric) for metric in self.metrics.test_metrics])}) / "
                f"indicate(current={self.checkpoint.indicate:.6f}, best={self.best_checkpoint.indicate:.6f})"
            )
        self.save_model(self.out / f'{self.out_prefix}_best.pt', self.best_checkpoint)

        self.checkpoint.set_states(self.model, self.optimizer)
        self.save_model(self.out / f'{self.out_prefix}_last.pt', self.checkpoint)

    def setup_training_model_and_optimizer(self):
        self.model.to(self.device)
        if self.half:
            from apex import amp
            # Initialization
            opt_level = 'O1'
            self._training_model, self._training_optimizer = \
                amp.initialize(self._training_model, self._training_optimizer, opt_level=opt_level, verbosity=0)

        if self.ddp:
            # try port number incrementally
            port = 9999
            while True:
                try:
                    dist.init_process_group(backend='nccl',
                                            init_method=f'tcp://127.0.0.1:{port}',
                                            world_size=1,
                                            rank=0)

                except RuntimeError as e:
                    if str(e) == "Address already in use":
                        port += 1
                        continue
                    else:
                        raise e
                break
            self._training_model = DistributedDataParallel(self._training_model, find_unused_parameters=True)

    def save_model(self, path: Path, checkpoint: Checkpoint):
        real_path = path

        state_dict = checkpoint.state_dict()
        torch.save(state_dict, real_path)

    def calc_indicate(self, train_rate) -> float:
        test_rate = 1 - train_rate
        test_loss = self.metrics.test_metrics[0]
        return self.loss_metric.get_value() ** train_rate * test_loss.get_value() ** test_rate

    def load_checkpoint(self, state_dict: dict):
        self.checkpoint.load(state_dict)
        self.start_epoch = self.checkpoint.epoch + 1
        self.model.load_state_dict(self.checkpoint.model_state)
        self.optimizer.load_state_dict(self.checkpoint.optimizer_state)

    def train_epoch(self, epoch: int):
        self._training_model.train()
        self.reset_all_metrics_states(self.metrics.train_metrics)

        for i, (data, target) in enumerate(self.data_loaders.train_loader):
            data = data.to(self.device)
            target = target.to(self.device)

            pred = self._training_model(data)
            evaluated = self.evaluate_metrics(pred, target, self.metrics.train_metrics)
            loss = self.loss_metric.get_tensor()
            if self.half:
                from apex import amp
                with amp.scale_loss(loss, self.optimizer) as scaled_loss:
                    scaled_loss.backward()
            else:
                loss.backward()

            self._training_optimizer.step()
            self._training_optimizer.zero_grad()

            mem_info = ""
            if self.device.type != "cpu":
                torch.cuda.synchronize()
                mem_info = f" / mem(allocated={torch.cuda.memory_allocated()}, cached={torch.cuda.memory_cached()})"

            print(
                "\r"
                f"epoch {epoch + 1}/{self.max_epochs} / "
                f"batch {i + 1}/{len(self.data_loaders.train_loader)} / "
                f"train ({self.get_evaluated_metrics_info(evaluated)})"
                + mem_info,
                end="")

    def test(self, no_grad: bool = True, loader: DataLoader = None, metrics: List[MetricBase] = None):
        self._training_model.eval()

        grad_policy = torch.no_grad if no_grad else torch.enable_grad
        loader = loader or self.data_loaders.test_loader
        metrics = metrics or self.metrics.test_metrics

        self.reset_all_metrics_states(metrics)

        with grad_policy():
            for i, (data, target) in enumerate(loader):
                data = data.to(self.device)
                target = target.to(self.device)

                pred = self._training_model(data)
                self.evaluate_metrics(pred, target, metrics)

    def reset_all_metrics_states(self, metrics: List[MetricBase]):
        for metric in metrics:
            metric.reset_states()

    def evaluate_metrics(self, pred: torch.Tensor, target: torch.Tensor, metrics: List[MetricBase]) -> Dict[str, float]:
        # The loss should calculate the gradient if gradient is enabled.
        loss_metric = metrics[0]
        result = {loss_metric.get_name(): loss_metric.evaluate(pred, target)}

        # Other metrics shouldn't calculate gradients so let them are detached.
        pred = pred.detach()
        target = target.detach()

        for metric in metrics[1:]:
            result[metric.get_name()] = metric.evaluate(pred, target)

        return result

    def get_evaluated_metrics_info(self, evaluated_infos: Dict[str, float]) -> str:
        return ', '.join([f'{name}={info:.6f}' for name, info in evaluated_infos.items()])
