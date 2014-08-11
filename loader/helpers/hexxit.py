import os
import fileinput
from loader.helpers.lib import forgeFixes


def modify(path, build):
    forgeFixes(path, build)

    config = os.path.join(path, 'config/InfernalMobs.cfg')
    replacements = {
        'useSimpleEntityClassnames=false': 'useSimpleEntityClassnames=true'
    }

    if not os.path.isfile(config):
        return True

    for line in fileinput.FileInput(config, inplace=1):
        for find, replace in replacements.iteritems():
            line = line.replace(find, replace)
