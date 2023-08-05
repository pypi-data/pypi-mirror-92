# Copyright The Compliancex Authors.
# SPDX-License-Identifier: Apache-2.0
#
# PYTHON_ARGCOMPLETE_OK  (Must be in first 1024 bytes, so if tab completion
# is failing, move this above the license)

# Copyright The Compliancex Authors.
# SPDX-License-Identifier: Apache-2.0
#
# PYTHON_ARGCOMPLETE_OK  (Must be in first 1024 bytes, so if tab completion
# is failing, move this above the license)

import argparse
import importlib
import logging
import os
import pdb
import sys
import traceback

import argcomplete

try:
    from setproctitle import setproctitle
except ImportError:
    def setproctitle(t):
        return None


def _key_val_pair(value):
    """
    Type checker to ensure that --field values are of the format key=val
    """
    if '=' not in value:
        msg = 'values must be of the form `header=field`'
        raise argparse.ArgumentTypeError(msg)
    return value


def _setup_logger(options):
    level = 3 + (options.verbose or 0) - (options.quiet or 0)

    if level <= 0:
        # print nothing
        log_level = logging.CRITICAL + 1
    elif level == 1:
        log_level = logging.ERROR
    elif level == 2:
        log_level = logging.WARNING
    elif level == 3:
        # default
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s: %(name)s:%(levelname)s %(message)s")

    external_log_level = logging.ERROR
    if level <= 0:
        external_log_level = logging.CRITICAL + 1
    elif level >= 5:
        external_log_level = logging.INFO

    logging.getLogger('botocore').setLevel(external_log_level)
    logging.getLogger('urllib3').setLevel(external_log_level)
    logging.getLogger('s3transfer').setLevel(external_log_level)
    logging.getLogger('urllib3').setLevel(logging.ERROR)


def setup_parser():
    parser = argparse.ArgumentParser(description="Compliancex - Cloud management")
    subs = parser.add_subparsers(title='commands', dest='subparser')

    health_check = subs.add_parser(
        "healthcheck", description="\n".join((
            "Checks the health of compliance infrastructure provisioning tool.",
        )),
        help="Checks the health of compliance infrastructure provisioning tool",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    health_check.set_defaults(command="compliance.endpoints.health_check")
    return parser


def main():
    parser = setup_parser()
    argcomplete.autocomplete(parser)
    options = parser.parse_args()
    if options.subparser is None:
        parser.print_help(file=sys.stderr)
        return sys.exit(2)

    # _setup_logger(options)

    # Support the deprecated -c option
    if getattr(options, 'config', None) is not None:
        options.configs.append(options.config)

    try:
        command = options.command
        if not callable(command):
            command = getattr(
                importlib.import_module(command.rsplit('.', 1)[0]),
                command.rsplit('.', 1)[-1])

        # Set the process name to something cleaner
        process_name = [os.path.basename(sys.argv[0])]
        process_name.extend(sys.argv[1:])
        setproctitle(' '.join(process_name))
        command()
    except Exception as error:
        # if not options.debug:
        #     raise
        traceback.print_exc()
        pdb.post_mortem(sys.exc_info()[-1])


if __name__ == '__main__':
    main()
