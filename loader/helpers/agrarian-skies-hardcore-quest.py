import os

def modify(path, build):
    dirs = [os.path.join(path, 'lib'), os.path.join(path, 'libraries')]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            open(os.path.join(d, '.keep'), 'a').close()

    os.remove(os.path.join(path, 'ServerStart.bat'))
    os.remove(os.path.join(path, 'ServerStart.sh'))