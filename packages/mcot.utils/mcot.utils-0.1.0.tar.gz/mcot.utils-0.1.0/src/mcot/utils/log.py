import os
import sys

from loguru import logger

SUBMITTED = os.getenv('FSLSUBALREADYRUN', default='') == 'true'


def get_level():
    """Returns the requested log level.

    0: no logging
    1: warning+
    2: info+
    3: debug+
    4: all+
    """
    levels = (
        None,
        "WARNING",
        "INFO",
        "DEBUG",
        0
    )
    if 'MCLOG' in os.environ:
        idx = int(os.environ['MCLOG'])
    else:
        idx = 3 if SUBMITTED else 2
    if idx > 4:
        idx = -1
    return levels[idx]


LOGSET = False


def setup_log(filename=None, replace=True):
    """Sets up the logger to log to the given filename.

    Sets up logging to:

    - If .log directory exists:

      - ~/.log/python.info (INFO and higher)
      - ~/.log/python.debug (DEBUG and higher)

    - stderr (minimum level is set by MCLOG; default values are DEBUG if submitted, INFO otherwise)

    - `filename` if provided

    :param filename: filename used in the logging (default: only set up logging to stdout/stderr and ~/.log directory)
    :param replace: if replace is True, replace the existing handlers
    """
    global LOGSET

    if replace:
        logger.remove(handler_id=None)

    if get_level() is None:
        return

    if filename is not None:
        logger.add(filename, level="DEBUG")
        logger.info(f'Added logging in {filename} ')

    if not LOGSET:
        logger.add(sys.stderr, level=get_level())

        log_directory = os.path.expanduser('~/.log')
        if os.path.isdir(log_directory):
            try:
                logger.add(os.path.join(log_directory, 'python.info'), rotation='1:00', level="INFO")
            except OSError:
                logger.exception("Failed to create .log/python.info file")
            try:
                logger.add(os.path.join(log_directory, 'python.debug'), rotation='1:00', level="DEBUG")
            except OSError:
                logger.exception("Failed to create .log/python.debug file")
        else:
            logger.info(f'Log directory {log_directory} not found; Skipping setup of global logging')

        LOGSET = True
        logger.debug(f'Finished setting up logging')
