# (c) 2020 Simon Rovder and others.
# This file is subject to the terms provided in 'LICENSE'.
"""
[Simon document this].
"""
import json
import argparse

from collections import defaultdict


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('merge',))
    parser.add_argument('output')
    parser.add_argument('inputs', nargs='+')
    args = parser.parse_args()

    with open(args.output, 'w') as outfile:
        merged = defaultdict(list)
        for path in args.inputs:
            with open(path, 'r') as infile:
                for k, v in json.load(infile).items():
                    merged[k].extend(v)

        json.dump(merged, outfile, ensure_ascii=False)

_main()
