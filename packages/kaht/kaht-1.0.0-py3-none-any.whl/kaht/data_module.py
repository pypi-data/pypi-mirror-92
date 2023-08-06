from typing import Generator, Iterable
from .base import Transferable
from tap import Tap


class DataTap(Tap):
    ...


class KahtDataModule:

    @classmethod
    def init_from_tap(cls, cfg: DataTap):
        raise NotImplementedError

    is_prepared: bool = False

    def prepare(self):
        raise NotImplementedError

    def train_dataloader(self, *args, **kwargs) -> Generator[Transferable, None, None]:
        raise NotImplementedError

    def test_dataloader(self) -> Iterable[Transferable]: ...

    def valid_dataloader(self) -> Iterable[Transferable]: ...
