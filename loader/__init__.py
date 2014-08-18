from .yggdrasil import Yggdrasil
from .resources import loaders


def run(config):
    y = Yggdrasil(config)
    y.run(loaders)