#!/usr/bin/env python
import argparse
import os

import autolnp
from autolnp.util import exit, load_source, touchdir

os.chdir(os.path.abspath(os.path.dirname(__file__)))

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--pack', help='Build package', type=str, metavar='Package ID')
parser.add_argument('-a', '--arch', '--platform', '--platforms',
    dest='platforms',
    help='Build for specified platforms (defaults to all paltforms)',
    type=str,
    nargs='+',
    choices=autolnp.pack.valid_platforms,
    default=autolnp.pack.valid_platforms)
args = parser.parse_args()
if args.pack is not None:
    if not os.path.isfile(args.pack):
        exit('Not found: %s', args.pack)
    pack = load_source(args.pack)
    assert hasattr(pack, 'main') and hasattr(pack.main, '__call__'), 'pack has no main() function'
    touchdir('builds')
    touchdir('downloads')
    args.platforms = list(set(args.platforms))
    autolnp.pack.create(name=os.path.splitext(os.path.basename(args.pack))[0],
        platforms=args.platforms, dest='builds')
else:
    print('No action taken - use "--help" for help')
