from .creeperrepo_loader import CreeperRepo
from .mojang_loader import Mojang
from .cauldron_loader import Cauldron

loaders = {
    'creeperrepo': CreeperRepo(),
    'mojang': Mojang(),
    'cauldron': Cauldron()
}