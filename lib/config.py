import os
import yaml


class Config():
    def __init__(self, **kwargs):
        self.skip = kwargs.get('skip', {})
        self.skip['paths'] = self.skip.get('paths', ('.git/', 'LICENSE.md'))
        self.skip['types'] = self.skip.get('types', ('bin', 'dat'))

        self.snippet = kwargs.get('snippet', {})
        self.snippet['lines_min'] = self.snippet.get('lines_min', 3)

        self.similarity = kwargs.get('similarity', {})
        self.similarity['identical'] = self.similarity.get('identical', True)
        self.similarity['ratio_fail'] = self.similarity.get('ratio_fail', 99)
        self.similarity['topk'] = self.similarity.get('topk', 1)

    def local(self):
        path = './.similarity.yml'

        if not os.path.isfile(path):
            return self

        with open(path) as fp:
            data = yaml.load(fp, Loader=yaml.SafeLoader)
            return Config(**data)
