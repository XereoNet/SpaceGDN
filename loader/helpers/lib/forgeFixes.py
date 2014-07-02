import os
import fileinput

def modify(path, build):
    config = os.path.join(path, 'config/forge.cfg')
    replacements = {
        'removeErroringEntities=false': 'removeErroringEntities=true',
        'removeErroringTileEntities=false': 'removeErroringTileEntities=true'
    }

    if not os.path.isfile(config):
        return True

    for line in fileinput.FileInput(config, inplace=True):
        for find, replace in replacements.iteritems():
            line = line.replace(find, replace)

        print line,