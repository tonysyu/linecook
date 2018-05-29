#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
`linecook` cli to prepare lines of text for easy consumption.

"""
from __future__ import print_function, unicode_literals

import argparse
import sys

from toolz.functoolz import compose

from .default_config import LINECOOK_CONFIG


def build_parser():
    formatter = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=formatter)

    parser.add_argument(
        'recipe', default='default', nargs='?',
        help="Collection of text transformations used to process text",
    )
    parser.add_argument(
        'text_stream', default=sys.stdin, nargs='?',
        type=argparse.FileType('r'),
        help="Text that will be transformed using the given recipe.",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    recipe = LINECOOK_CONFIG['recipes'][args.recipe]
    # Reverse recipe since we want transforms earlier in the list applied
    # first, but `toolz.functoolz.compose` runs it in the opposite direction.
    process_text = compose(*reversed(recipe))
    for line in args.text_stream:
        # Newlines are usually part of the input line so set `end=''`.
        print(process_text(line), end='')


if __name__ == '__main__':
    main()
