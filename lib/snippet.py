import difflib


class Snippet(object):
    def __init__(self, **kwargs):
        self.data = kwargs.get('data')

    def match_ratio(self, rival):
        return round(
            difflib.SequenceMatcher(None, self.data, rival.data).ratio() * 100.0,
            3
        )
