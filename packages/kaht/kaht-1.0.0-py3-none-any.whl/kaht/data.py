from .base import Transferable
import torch
import random


class BatchBase(Transferable):
    def to(self, gpu: torch.device):
        for k, v in vars(self).items():
            if isinstance(v, torch.Tensor):
                setattr(self, k, v.to(gpu))
            elif isinstance(v, list):
                _i = random.choice(v)
                if isinstance(_i, int) or isinstance(_i, float):
                    setattr(self, k, torch.tensor(v, device=gpu))
            else:
                continue
