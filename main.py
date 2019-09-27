#!/usr/bin/env python3

import sys

from lib.config import Config
from lib.directory import Directory


if __name__ == '__main__':
    config = Config().local()

    files = []

    dir = Directory('./')
    for file in dir.files_iter(config.skip):
        file.snippets = list(file.parse(config.snippet))
        files.append(file)

    paired = []
    similars = []

    for file_a in files:
        for snippet_a in file_a.snippets:
            for file_b in files:
                if (
                    file_a == file_b or
                    (file_a, file_b) in paired or
                    (file_b, file_a) in paired
                ):
                    continue

                for snippet_b in file_b.snippets:
                    ratio = snippet_a.match_ratio(snippet_b)

                    similars.append({
                        'files': (file_a, file_b),
                        'snippets': (snippet_a, snippet_b),
                        'ratio': ratio
                    })

                paired.append((file_a, file_b))

    failed = False
    for similar in similars:
        ratio = similar.get('ratio')

        if config.similarity.get('identical') and ratio == 100.0:
            continue

        if ratio > config.similarity.get('ratio_fail'):
            failed = True

            file_a, file_b = similar.get('files')
            snippet_a, snippet_b = similar.get('snippets')

            print('# {}%\t{}\t{}'.format(ratio, file_a.path, file_b.path))
            print('a\t{}'.format(snippet_a.data.replace('\n', '\na\t')))
            print('#')
            print('b\t{}'.format(snippet_b.data.replace('\n', '\nb\t')))
            print('')

    if not failed:
        print('# Here\'s top {} similars for informational purposes'.format(config.similarity.get('topk')))

        for similar in sorted(similars, key=lambda x: x.get('ratio', 0), reverse=True)[:config.similarity.get('topk')]:
            ratio = similar.get('ratio')

            file_a, file_b = similar.get('files')
            snippet_a, snippet_b = similar.get('snippets')

            print('# {}%\t{}\t{}'.format(ratio, file_a.path, file_b.path))
            print('a\t{}'.format(snippet_a.data.replace('\n', '\na\t')))
            print('#')
            print('b\t{}'.format(snippet_b.data.replace('\n', '\nb\t')))
            print('')

        print('# Check passed')
    else:
        print('# Check FAILED')
        sys.exit(1)
