from abc import ABC
from typing import Protocol, List, Any, Generator, Union, Iterable, Literal, Callable
from torch.utils.data.dataloader import DataLoader
from torch.optim.optimizer import Optimizer
import torch
from logging import Logger
from .base import Transferable, SaveDelegate
from typing import Optional
from .optim import LearningRateMixIn
import numpy as np
import os
from tap import Tap
from .config import ModelTap

MODE = Literal['eval', 'train']
SAVED_SUFFIX = Literal['_best', '_latest']
TEST_CHOICES = Literal['best', 'latest']


class LoggerMixin:
    logger: Optional[Logger] = None
    log: Callable
    warn: Callable
    critical: Callable
    debug: Callable

    def configure_logger(self, _logger: Logger):
        self.logger = _logger
        self.log = _logger.info
        self.warn = _logger.warning
        self.critical = _logger.critical
        self.debug = _logger.debug


class KahtDataModule:
    is_prepared: bool = False

    def prepare(self):
        raise NotImplementedError

    def train_dataloader(self, *args, **kwargs) -> Generator[Transferable, None, None]:
        raise NotImplementedError

    def test_dataloader(self) -> Iterable[Transferable]: ...

    def valid_dataloader(self) -> Iterable[Transferable]: ...


class ModuleMixIn:
    mode: MODE

    save_delegate: SaveDelegate

    def will_train(self, *args, **kwargs): ...

    def on_train_one_step_start(self, logger: Logger): ...

    def train_one_step(self, batch) -> torch.Tensor:
        raise NotImplementedError

    def configure_optimizer(self) -> Union[Optimizer, List[Optimizer]]: ...

    def train_steps_end(self, outputs: List[Any]): ...

    def on_train_end(self): ...

    def will_test(self, *args, **kwargs): ...

    def test_one_task(self, batch): ...

    def on_test_end(self, outpus: List[Any]): ...

    def will_valid(self, *args, **kwargs): ...

    def valid_one_task(self, batch) -> Any: ...

    def on_valid_end(self, outpus: List[Any]): ...

    def params_for_clip(self): ...

    def report_every(self, losses: Iterable): ...

    def save(self, suffix: SAVED_SUFFIX, *args):
        """ Save and return saved result.
        :param suffix:
        :return:
        """
        raise NotImplementedError

    @property
    def training(self) -> bool:
        return self.mode == 'train'

    def switch(self, mode: MODE):
        raise NotImplementedError


class KahtModule(torch.nn.Module, LoggerMixin, LearningRateMixIn, ABC):
    mode: MODE

    save_delegate: SaveDelegate

    # set true if backward in module; else backward in trainer
    manual_backward: bool = False

    trainer = None

    best_loss = np.inf

    model_name: str = 'KahtModule'

    _current_epoch: int = 0

    should_stop_training: bool = False

    @classmethod
    def init_from_tap(cls, cfg: ModelTap):
        if os.path.exists(cfg.ckpt):
            return cls.load_checkpoint(cfg.ckpt)
        else:
            raise NotImplementedError

    def will_train(self, *args, **kwargs):
        ...

    def on_train_one_step_start(self, logger: Logger):
        ...

    def sanity_train_one_step(self, batch) -> torch.Tensor:
        return self.train_one_step(batch)

    def train_one_step(self, task_batch) -> torch.Tensor:
        raise NotImplementedError

    def train_steps_end(self, outputs: List[Any]):
        ...

    def on_train_end(self):
        ...

    def will_test(self):
        ...

    def test_one_task(self, batch) -> Any:
        ...

    def on_test_end(self, outputs: list[Any]):
        ...

    def will_valid(self):
        ...

    def valid_one_task(self, batch) -> Any:
        ...

    def on_valid_end(self, outputs: List[Any]):
        ...

    def will_eval(self):
        ...

    def eval_one_task(self, batch) -> Any:
        ...

    def on_eval_end(self, outputs: list[Any], on: Literal['valid', 'test'] = 'test'):
        ...

    def params_for_clip(self):
        parameters = filter(lambda p: p.requires_grad, self.parameters())
        return parameters

    def report_every(self, losses: Iterable):
        ...

    def __init__(self):
        super(KahtModule, self).__init__()

    @property
    def home(self):
        if self.trainer:
            return self.trainer.home_dir
        else:
            return os.getcwd()

    @property
    def current_epoch(self):
        return self.trainer.current_step

    def switch(self, mode: MODE):
        if mode == 'eval':
            self.eval()
        elif mode == 'train':
            self.train()

    def save_checkpoint(self, filename: str):
        torch.save(self, filename)

    @classmethod
    def load_checkpoint(cls, filename: str):
        model = torch.load(filename, map_location=torch.device('cpu'))
        if isinstance(model, KahtModule):
            return model
        else:
            raise RuntimeError(f"Checkpoint type not match! Assume KhatModule get {type(model)}")

    def save(self, suffix: SAVED_SUFFIX, other: str = ''):
        _fn = f"{self.model_name}_EPO{self.current_epoch}{suffix}{other}.ckpt"
        fn = os.path.join(self.home, _fn)
        self.save_checkpoint(fn)
        self.save_delegate.on_save(fn)
