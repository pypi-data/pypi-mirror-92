from torch.optim.lr_scheduler import LambdaLR
from torch.optim import Optimizer
from typing import Optional, Union


class LearningRateMixIn:
    def configure_lr(self, lr: float):
        """
        Default inplementation return bare lr
        :param lr: given the learning rate
        :return:
        """
        return lr

    def configure_scheduler(self, optims: Union[Optimizer, list[Optimizer]]) -> Optional[LambdaLR]:
        """
        Provide schedulers for trainer
        :return:
        """
        return None

    def configure_optimizers(self) -> Union[Optimizer, list[Optimizer]]:
        raise NotImplementedError
