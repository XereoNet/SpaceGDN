from .creeperrepo_loader import CreeperRepo
from .mojang_loader import Mojang
from .technic_loader import Technic
from .direct_loader import Direct
from .jenkins_maven_loader import JenkinsMaven

loaders = {
    'creeperrepo': CreeperRepo(),
    'mojang': Mojang(),
    'technic': Technic(),
    'direct': Direct(),
    'jenkins_maven': JenkinsMaven()
}
