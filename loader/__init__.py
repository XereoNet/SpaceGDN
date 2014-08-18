from .yggdrasil import Yggdrasil
from .resources import loaders


def run(config, only_use=None):
    y = Yggdrasil(config)
    to_load = []
    if only_use is None:
        to_load = loaders.values()
    else:
        for key, loader in loaders.items():
            if key in only_use:
                to_load.append(loader)

    y.run(to_load)