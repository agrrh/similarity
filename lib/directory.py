import os

from lib.file import File


class Directory(object):
    def __init__(self, path):
        self.path = path

    def files_iter(self, config):
        for root, dirs, files in os.walk(self.path):
            # Exclude by paths
            if [path for path in config.get('paths') if path in root + '/']:
                continue

            # Exclude by extensions
            files = filter(
                lambda x: not bool([type for type in config.get('types') if x.endswith(type)]),
                files
            )

            for file in files:
                path = os.path.join(root, file)
                yield File(path)
