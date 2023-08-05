#!/usr/bin/env python
"""
run.py [options] ASV_COMMAND..

Convenience wrapper around the ``asv`` command; just sets environment
variables and chdirs to the correct place etc.

"""

import os
import sys
import subprocess
import json
import shutil
import argparse
import sysconfig
import errno


EXTRA_PATH = ['']


def main():
    class ASVHelpAction(argparse.Action):
        nargs = 0
        def __call__(self, parser, namespace, values, option_string=None):
            sys.exit(run_asv(['--help']))

    p = argparse.ArgumentParser(usage=__doc__.strip())
    p.add_argument('--help-asv', nargs=0, action=ASVHelpAction,
        help="""show ASV help""")
    p.add_argument('asv_command', nargs=argparse.REMAINDER)
    args = p.parse_args()

    sys.exit(run_asv(args.asv_command))


def run_asv(args):
    cwd = os.path.abspath(os.path.dirname(__file__))

    repo_dir = os.path.join(cwd, 'refnx')

    cmd = ['asv'] + list(args)
    env = dict(os.environ)

    # Inject ccache/f90cache paths
    if sys.platform.startswith('linux'):
        env['PATH'] = os.pathsep.join(EXTRA_PATH + env.get('PATH', '').split(os.pathsep))

    # Check refnx version if in dev mode; otherwise clone and setup results
    # repository
    if args and (args[0] == 'dev' or '--python=same' in args):
        import refnx
        print("Running benchmarks for refnx version %s at %s" % (refnx.__version__, refnx.__file__))

    # Run
    try:
        return subprocess.call(cmd, env=env, cwd=cwd)
    except OSError as err:
        if err.errno == errno.ENOENT:
            print("Error when running '%s': %s\n" % (" ".join(cmd), str(err),))
            print("You need to install Airspeed Velocity https://spacetelescope.github.io/asv/")
            print("to run refnx benchmarks")
            return 1
        raise


if __name__ == "__main__":
    sys.exit(main())
