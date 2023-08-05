#!/usr/bin/env python
import os
import sys
from pathlib import Path

#: Default configuration path for Mailman Web.
MAILMAN_WEB_CONFIG = '/etc/mailman3/settings.py'

def setup():
    """Setup default environment variables for Mailman web."""
    # Make sure to setdefault and not set because we don't want to override if
    # a user specified the settings module.
    os.environ.setdefault("MAILMAN_WEB_CONFIG", MAILMAN_WEB_CONFIG)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


def main():
    setup()

    os.environ['DJANGO_IS_MANAGEMENT_COMMAND'] = '1'
    if not os.path.exists(MAILMAN_WEB_CONFIG):
        # If the configuration does not exist, print that and exit with error
        # code 1.
        print('Mailman web configuration file at {} does not exist'.format(
            MAILMAN_WEB_CONFIG), file=sys.stderr)
        print('Modify "MAILMAN_WEB_CONFIG" environment variable to point at '
              'settings.py', file=sys.stderr)
        sys.exit(1)
    # Add configuration file's parent directory to sys.path.
    config_path = Path(os.environ['MAILMAN_WEB_CONFIG']).resolve()
    sys.path.append(str(config_path.parent))
    # Set configuration file's name as DJANGO_SETTINGS_MODULE if it isn't settings already.
    if not config_path.stem == 'settings':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', config_path.stem)
    # Now simply execute the command.
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
