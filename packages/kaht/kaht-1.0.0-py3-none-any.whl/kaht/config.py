import toml
from tap import Tap
import torch


class TapMixIn(Tap):
    @classmethod
    def auto_init(cls):
        return cls().parse_args()

    def to_dict(self, *skip_keys):
        result = self.as_dict()
        result.pop('auto_init')
        result.pop('to_dict')
        for k in skip_keys:
            if k in result.keys():
                result.pop(k)
        return dict(sorted(result.items()))


_KEY_SET = {'model', 'trainer', 'data'}


class TOMLMixIn:
    def load_toml(self, filename: str):
        raise NotImplementedError

    def save_toml(self, filename: str):
        raise NotImplementedError


class ModelTap(TapMixIn):
    ckpt: str = ''  # checkpoint for model


class DataTap(TapMixIn):
    ...


class TrainerTap(TapMixIn):
    debug: bool = False
    min_steps: int = 1
    max_steps: int = 1
    valid_interval: int = 1
    report_interal: int = 50
    grad_clip: float = -1.0
    log_dir: str = 'outputs/'
    out_dir: str = 'outputs/'
    log_file: str = '/dev/null'  # custom your log file
    name: str = 'KahtTrainer'
    gpu: int = -1
    seed: int = 8964
    accumulated_steps: int = 1
    no_sanity: bool = False
    sanity: bool = False
    prefix: str = ''
    home: str = '.'
    test: bool = False

    @property
    def device(self):
        return torch.device(
                f"cuda:{self.gpu}" if self.gpu >= 0 and torch.cuda.is_available() else 'cpu')


class KahtTap(TOMLMixIn):
    # todo: test
    trainer: TrainerTap = TrainerTap()
    model: ModelTap = ModelTap()
    data: DataTap = DataTap()

    def __init__(self, data: DataTap, model: ModelTap):
        self.data = data
        self.model = model

    def to_dict(self, *args):
        result = dict()
        result['data'] = self.data.to_dict(*args)
        result['model'] = self.model.to_dict(*args)
        result['trainer'] = self.trainer.to_dict('device', *args)
        return result

    def __str__(self):
        result = dict()
        result['data'] = self.data.to_dict()
        result['model'] = self.model.to_dict()
        result['trainer'] = self.trainer.to_dict('device')
        return str(result)

    def save_toml(self, filename: str, *skip_keys):
        result = dict()
        result['data'] = self.data.to_dict(*skip_keys)
        result['model'] = self.model.to_dict(*skip_keys)
        result['trainer'] = self.trainer.to_dict('device', *skip_keys)

        toml.dump(result, open(filename, 'w'))

    def load_toml(self, filename: str):
        result = toml.load(filename)
        for k, v in result.items():
            if k not in _KEY_SET:
                pass
            elif k == 'model':
                self.model.from_dict(v)
            elif k == 'trainer':
                self.trainer.from_dict(v)
            elif k == 'data':
                self.data.from_dict(v)
        return self



