import os
import yaml


class Config(object):
    def __init__(self, **kwargs):
        self.skip = kwargs.get('skip', {})
        self.skip['paths'] = self.skip.get('paths', ('.git/', 'LICENSE.md'))
        self.skip['types'] = self.skip.get('types', ('bin', 'dat'))

        self.snippet = kwargs.get('snippet', {})
        self.snippet['lines_min'] = self.snippet.get('lines_min', 3)

        self.similarity = kwargs.get('similarity', {})
        self.snippet['identical'] = self.similarity.get('identical', True)
        self.snippet['ratio_fail'] = self.similarity.get('ratio_fail', 99)

    def local(self):
        path = './.similarity.yml'

        if not os.path.isfile(path):
            return self

        with open(path) as fp:
            data = yaml.load(fp, Loader=yaml.SafeLoader)
            return Config(**data)
