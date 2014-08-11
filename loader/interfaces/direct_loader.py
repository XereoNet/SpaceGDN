class loader_direct:

    def __init__(self):
        pass

    def load(self, channel, _):
        builds = []

        builds.append({
            'version': channel['version'],
            'size': None,
            'checksum': None,
            'url': channel['url'],
            'build': 1
        })

        return builds
