import hashlib
import datetime
from tap import Tap


def uuid(src: str = 'MAKE ANTARX GREAT AGAIN', cut: int = 4):
    now_str = str(datetime.datetime.now())
    sha = hashlib.sha256(now_str.encode())
    sha.update(src.encode())
    return str(sha.hexdigest())[:cut].upper()


def time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d-%Hh%Mm%Ss")


class TapMixIn(Tap):
    @classmethod
    def auto_init(cls):
        return cls().parse_args()
