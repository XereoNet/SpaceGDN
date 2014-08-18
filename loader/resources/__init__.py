from .creeperrepo_loader import CreeperRepo
from .mojang_loader import Mojang

loaders = {
    'creeperrepo': CreeperRepo(),
    'mojang': Mojang()
}