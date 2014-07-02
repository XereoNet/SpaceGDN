import os
from loader.helpers.lib import forgeFixes

def modify(path, build):
    forgeFixes(path, build)

    dirs = [os.path.join(path, 'libs')]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            open(os.path.join(d, '.keep'), 'a').close()