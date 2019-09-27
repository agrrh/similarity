#!/usr/bin/env python3

import sys

from lib.config import Config
from lib.directory import Directory


if __name__ == '__main__':
    config = Config().local()

    files = []

    # TODO use argparse
    # TODO add command to diff 2 files
    # TODO add summary flag
    try:
        path = sys.argv[1]
    except IndexError:
        path = ''

    dir = Directory(path or './')
    for file in dir.files_iter(config.skip):
        file.snippets = list(file.parse(config.snippet))
        files.append(file)

    print('Analyzing content of "{}"'.format(dir.path))
    print('Satisfactory files found: {}'.format(len(files)))
    print('Please be patient ...')

    paired = []
    similars = []

    total = sum([len(file.snippets) for file in files]) ** 2
    i = 0

    for file_a in files:
        for snippet_a in file_a.snippets:
            for file_b in files:
                if (
                    file_a == file_b or  # FIXME compare different snippets from one file
                    (file_a, file_b) in paired or
                    (file_b, file_a) in paired
                ):
                    i += len(file_b.snippets)
                    continue

                for snippet_b in file_b.snippets:
                    # TODO parallelism?
                    ratio = snippet_a.match_ratio(snippet_b)

                    similars.append({
                        'files': (file_a, file_b),
                        'snippets': (snippet_a, snippet_b),
                        'ratio': ratio
                    })

                    i += 1

                paired.append((file_a, file_b))

                print('\r{}% ~{}/{}'.format(round(i / total * 100.0, 1), i, total), end='')
    print('')

    # TODO move this to separate class
    failed = 0
    for similar in similars:
        ratio = similar.get('ratio')

        if config.similarity.get('identical') and ratio == 100.0:
            continue

        if ratio > config.similarity.get('ratio_fail'):
            failed += 1

            file_a, file_b = similar.get('files')
            snippet_a, snippet_b = similar.get('snippets')

            print('RATIO {}%'.format(ratio))
            print('')
            print('A {}'.format(file_a.path))
            print('')
            print('\t{}'.format(snippet_a.data.replace('\n', '\n\t')))
            print('')
            print('B {}'.format(file_b.path))
            print('')
            print('\t{}'.format(snippet_b.data.replace('\n', '\n\t')))
            print('')
            print('')

    if failed == 0:
        print('TOP{} similars for INFO purposes'.format(config.similarity.get('topk')))
        print('')

        for similar in sorted(similars, key=lambda x: x.get('ratio', 0), reverse=True)[:config.similarity.get('topk')]:
            ratio = similar.get('ratio')

            file_a, file_b = similar.get('files')
            snippet_a, snippet_b = similar.get('snippets')

            print('RATIO {}%'.format(ratio))
            print('')
            print('A {}'.format(file_a.path))
            print('')
            print('\t{}'.format(snippet_a.data.replace('\n', '\n\t')))
            print('')
            print('B {}'.format(file_b.path))
            print('')
            print('\t{}'.format(snippet_b.data.replace('\n', '\n\t')))
            print('')
            print('')

        print('OK, check passed')
    else:
        print('ERROR, check FAILED for {} snippets'.format(failed))
        sys.exit(1)
