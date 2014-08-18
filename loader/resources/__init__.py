from .creeperrepo_loader import CreeperRepo
from .mojang_loader import Mojang
from .cauldron_loader import Cauldron
from .craftbukkit_loader import CraftBukkit

loaders = {
    'creeperrepo': CreeperRepo(),
    'mojang': Mojang(),
    'cauldron': Cauldron(),
    'craftbukkit': CraftBukkit()
}