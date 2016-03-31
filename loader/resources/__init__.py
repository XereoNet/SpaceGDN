from .creeperrepo_loader import CreeperRepo
from .mojang_loader import Mojang
from .cauldron_loader import Cauldron
from .craftbukkit_loader import CraftBukkit
from .technic_loader import Technic
from .direct_loader import Direct
from .jenkins_maven_loader import JenkinsMaven

loaders = {
    'creeperrepo': CreeperRepo(),
    'mojang': Mojang(),
    'cauldron': Cauldron(),
    'craftbukkit': CraftBukkit(),
    'technic': Technic(),
    'direct': Direct(),
    'jenkins_maven': JenkinsMaven()
}
