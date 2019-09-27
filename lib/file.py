from lib.snippet import Snippet


class File(object):
    def __init__(self, path):
        self.path = path
        self.snippets = []

    def content(self):
        with open(self.path) as fp:
            return fp.read()

    def parse(self, config):
        '''
        Split file content into snippets
        '''
        lines = self.content().split('\n')

        blocks = []
        block = []
        for line in lines:
            if not block and not line:
                continue

            if not line:
                blocks.append(block)
                block = []
                continue

            if line:
                block.append(line)

        snippets = []

        # From beginning
        buf = []
        for block in blocks:
            buf.extend(block)

            if len(buf) > config.get('lines_min'):
                snippets.append(buf)
                buf = []
            else:
                buf.append('')

        while buf:
            tmp = snippets.pop()
            tmp.extend([''] + buf[:-1])
            buf = tmp

            if len(buf) > config.get('lines_min'):
                snippets.append(buf)
                buf = []

        for snippet in snippets:
            self.snippets.append(snippet)
            yield Snippet(data='\n'.join(snippet))
