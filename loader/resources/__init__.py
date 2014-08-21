from .creeperrepo_loader import CreeperRepo
from .mojang_loader import Mojang
from .cauldron_loader import Cauldron
from .craftbukkit_loader import CraftBukkit
from .technic_loader import Technic

loaders = {
    'creeperrepo': CreeperRepo(),
    'mojang': Mojang(),
    'cauldron': Cauldron(),
    'craftbukkit': CraftBukkit(),
    'technic': Technic()
}