"""
Contains globals used for time and duration classes.
"""

from datetime import datetime
import re

__program__ = 'time_globals.py'
__author__  = 'Forrest Ridenhour'
__project__ = 'Mars2020'
__version__ = '1.0'
__dependencies__ = 'datetime'


UTC_REGEX_STRING = \
    '(?P<year>\d{4})-' \
    '(?P<doy>\d\d?\d?)T' \
    '(?P<hours>\d\d?):' \
    '(?P<minutes>\d\d?):' \
    '(?P<seconds>\d\d?)\.?' \
    '(?P<decimal>(\d+))?'

LMST_REGEX_STRING = \
    '(Sol|sol|SOL)?-?\s*' \
    '(?P<sol>\d+)' \
    '(M|\s+)' \
    '(?P<time_of_day>' \
    '(?P<hours>[0-1][0-9]|[2][0-3]):' \
    '(?P<minutes>[0-5][0-9]):' \
    '(?P<seconds>[0-5][0-9])\.?' \
    '(?P<decimal>(\d+))?)'

DURATION_REGEX_STRING = \
    '(?P<sign>-)?' \
    '(?:(?P<days>\d+)?T|T?)' \
    '(?P<time_of_day>(?P<hours>\d+):' \
    '(?P<minutes>\d+):' \
    '(?P<full_seconds>' \
    '(?P<seconds>\d+)' \
    '(?:\.(?P<decimal>\d+))?))'

MARS_DURATION_REGEX_STRING = \
    '(?P<sign>-)?' \
    '(?P<sols>\d+)?M' \
    '(?P<hours>\d+):' \
    '(?P<minutes>\d+):' \
    '(?P<seconds>\d+)' \
    '(?:\.(?P<decimal>\d+))?'

SPICE_LMST_REGEX_STRING = \
    '\d\/' \
    '(?P<sol>\d+):' \
    '(?P<hour>\d+):' \
    '(?P<min>\d+):' \
    '(?P<sec>\d+):' \
    '(?P<subsec>\d+)'

EPOCH_RELATIVE_REGEX_STRING = '(?P<epoch_name>\\w+)\\s*(?P<relative_sign>[+-])\\s*(?P<offset>' + DURATION_REGEX_STRING + ')'

SCLK_FLOAT_REGEX_STRING = '(?P<seconds>\d+)\.(?P<subsec>\d+)'
SCLK_REGEX_STRING = '\d\/(?P<seconds>\d+)-(?P<fraction>\d+)'


UTC_REGEX                   = re.compile(UTC_REGEX_STRING, re.VERBOSE)
UTC_EXACT_REGEX             = re.compile('^' + UTC_REGEX_STRING + '$', re.VERBOSE)

LMST_REGEX                  = re.compile(LMST_REGEX_STRING, re.VERBOSE)
LMST_EXACT_REGEX            = re.compile('^' + LMST_REGEX_STRING + '$', re.VERBOSE)

DURATION_REGEX              = re.compile(DURATION_REGEX_STRING, re.VERBOSE)
DURATION_EXACT_REGEX        = re.compile('^' + DURATION_REGEX_STRING + '$', re.VERBOSE)

MARS_DURATION_REGEX         = re.compile(MARS_DURATION_REGEX_STRING, re.VERBOSE)
MARS_DURATION_EXACT_REGEX   = re.compile('^' + MARS_DURATION_REGEX_STRING + '$', re.VERBOSE)

SPICE_LMST_REGEX            = re.compile(SPICE_LMST_REGEX_STRING, re.VERBOSE)
SPICE_LMST_REGEX_EXACT      = re.compile('^' + SPICE_LMST_REGEX_STRING + '$', re.VERBOSE)

SCLK_REGEX                  = re.compile(SCLK_REGEX_STRING, re.VERBOSE)
SCLK_REGEX_EXACT            = re.compile('^' + SCLK_REGEX_STRING + '$', re.VERBOSE)

SCLK_FLOAT_REGEX            = re.compile(SCLK_FLOAT_REGEX_STRING, re.VERBOSE)
SCLK_FLOAT_REGEX_EXACT      = re.compile('^' + SCLK_FLOAT_REGEX_STRING + '$', re.VERBOSE)

EPOCH_RELATIVE_REGEX        = re.compile(EPOCH_RELATIVE_REGEX_STRING, re.VERBOSE)
EPOCH_RELATIVE_REGEX_EXACT  = re.compile('^' + EPOCH_RELATIVE_REGEX_STRING + '$', re.VERBOSE)

# set epoch to be used by datetime to seconds since epoch
EPOCH = datetime.utcfromtimestamp(0)

# Global Constants #
SECONDS_PER_MINUTE      = 60
SECONDS_PER_HOUR        = 60*60
SECONDS_PER_DAY         = 60*60*24
MINUTES_PER_DAY         = 60*24
HOURS_PER_DAY           = 24
MICROSECONDS_PER_SECOND = 1000000
MARS_TIME_SCALE         = 1.02749125170
MAX_OUTPUT_LENGTH = 35  # this probably just needs to be greater than the max, so 35 is fine?

# format strings
UTC_FMT_TRUNCATED       = '%Y-%jT%H:%M:%S'
UTC_FMT_FULL            = '%Y-%jT%H:%M:%S.%f'

EARTH_NAIF_ID = 399
MARS_NAIF_ID = 499