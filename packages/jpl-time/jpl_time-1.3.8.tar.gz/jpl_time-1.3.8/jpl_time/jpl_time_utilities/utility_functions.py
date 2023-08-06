# -*- coding: utf-8 -*-

"""
This file contains various utility functions used by jpl_time and jpl_time_utilities.
"""

import sys
import time

# in case █ doesn't work
BACKUP_BAR_UNIT = '*'

def progress_bar(count, total, message = '', bar_unit = '█', remaining_unit = '-', bar_length = 50):
    """Create terminal progress bar by calling this function after each iteration of the main loop."""
    percent = round(count * 100.0 / total, 1)
    filled = int(round(bar_length * count / float(total)))

    # \r is the carriage return and returns the position to the beginning of the line
    try:
        bar = filled * bar_unit + remaining_unit * (bar_length - filled)
        sys.stdout.write('\rProgress: |{}| {}% {}'.format(bar, percent, message))
    except UnicodeEncodeError:
        bar = filled * BACKUP_BAR_UNIT + remaining_unit * (bar_length - filled)
        sys.stdout.write('\rProgress: |{}| {}% {}'.format(bar, percent, message))

    # flush forces the script to write to the terminal, even if it would normally wait before doing so
    sys.stdout.flush()
    # end of progress bar -> print new line
    if count == total:
        sys.stdout.write('\n')
        sys.stdout.flush()
    time.sleep(.1)