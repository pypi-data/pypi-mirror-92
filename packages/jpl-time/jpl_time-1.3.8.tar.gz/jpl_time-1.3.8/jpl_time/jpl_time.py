"""
The Time class is used to convert between times or perform time math.
Wraps several SPICE calls, such as OWLT, UTC->LMST, UTC->LTST, etc.
Under the hood, all times are converted to ET seconds since epoch
using SPICE, and all methods which return a time string also use SPICE,
so leap seconds are always accounted for. When adding/subtracting
durations, ET seconds are converted to TAI seconds and then back to
ET seconds.

Usage:
This module is meant to be imported into a script or used in the python
terminal interpreter:
from jpl_time import Time

You will need to load kernels in order to use the time class, which is
done by calling Time.load_kernels(kernel_list), where the kernel_list is
a list of paths to SPICE kernels.

To avoid having to ensure that load_kernels is called before any time objects
are created, one can extend the Time class and load the kernels in that file.


Once kernels are loaded and the spacecraft ID is set, you can create a time
object such as:
t = Time('2019-150T12:00:00)

You can then add durations to the time object, such as:
d = Duration('02:00:00')
t2 = t + d
t2.to_utc() == '2019-150T14:00:00'

You can call various methods which wrap SPICE, such as:
t.to_lmst()
t.to_sclkd()
t.to_ltst()
t.to_ert()
t.to_ett()

It can also handle time zones:
t.to_pt()
t.to_timezone('Asia/Kolkata')

You can subtract two times to get a duration object:
d = t1 - t2
d.to_string()

You can call static methods to convert from LMST, SCLKD, etc.
t = Time.from_sclkd(sclkd_value)
t = Time.from_lmst('Sol-0025M00:00:00')

You can also use static methods to get the owlt at a specific time:
d = downleg(t)
u = upleg(t)
o = owlt(t, -168, 399)

There are also methods to round time objects:
t = '2019-155T13:45:28'
t.round(Duration('00:01:00').to_utc()   = '2019-155T13:45:00'
t.round(Duration('01:00:00').to_utc()   = '2019-155T14:00:00'
t.ceil( Duration('01:00:00').to_utc()   = '2019-155T14:00:00'
t.floor(Duration('01:00:00').to_utc()   = '2019-155T13:00:00'

The Duration class is used to convert between Mars and Earth durations,
perform math with Time and Durations, and format Durations.
Under the hood, all times are converted to seconds.

Usage:
This module is meant to be imported into a script or used in the python
terminal interpreter:
from Duration import Duration

You create a duration object such as:
d = Duration('02:00:00')

You can then perform math operations, such as adding, subtracting,
multiplying, or dividing:
d2 = d + Duration('01:30:00')
d2.to_string() = '03:30:00'

d3 = d - Duration('03:00:00')
d3.to_string() = '-01:00:00'

d4 = d * 3
d4.to_string() = '06:00:00'

d5 = d / 2
d5.to_string() = '01:00:00'

d6 = d / Duration('01:00:00')
d6 = 2

You can also convert to a mars duration:
d.to_mars_dur() = '01:56:47.359'

You can also create a Duration object using a timedelta,
float, int, Duration object, or an earth or mars duration
string:
d = Duration(timedelta(seconds=100))
d = Duration(1)
d = Duration(10.0)
d = Duration('00:01:00')
d = Duration('M01:00:00')
d = Duration(Duration(1))

There are also methods to round Duration objects:
d = '155T13:45:28'
d.round(Duration('00:01:00').to_string()   = '155T13:45:00'
d.round(Duration('01:00:00').to_string()   = '155T14:00:00'
d.ceil( Duration('01:00:00').to_string()   = '155T14:00:00'
d.floor(Duration('01:00:00').to_string()   = '155T13:00:00'
"""

import re
import argparse
import os
from datetime import datetime, timedelta, date
import pytz
import spiceypy as spice
import sys
import math

# the script jpl_time.py and jpl_time scripts need different import paths

try:
    from jpl_time_utilities import time_globals
    from jpl_time_utilities import chronos_input_parsing
    from jpl_time_utilities import fetch_latest_kernels

except ImportError:
    from jpl_time.jpl_time_utilities import time_globals
    from jpl_time.jpl_time_utilities import chronos_input_parsing
    from jpl_time.jpl_time_utilities import fetch_latest_kernels

__program__ = 'jpl_time.py'
__author__ = 'Forrest Ridenhour'
__project__ = 'Mars2020'
__version__ = '1.3.8'
__dependencies__ = 'time_globals.py, spiceypy, pytz, datetime'

PACIFIC_TIME_ZONE = 'America/Los_Angeles'
PST_TIME_ZONE = 'Etc/GMT+8'
PDT_TIME_ZONE = 'Etc/GMT+7'
ISRO_TIME_ZONE = 'Asia/Kolkata'

GPST_EPOCH = '1980-006T00:00:00'
ET_EPOCH = '2000-001T11:58:55.816'
DEFAULT_REFERENCE_TIME = '2020-001T00:00:00'
ALLOWED_INPUT_TYPES = ['scet', 'utc', 'isoc', 'ert', 'ett', 'gps', 'pt', 'pst', 'pdt',
                       'et', 'sclk', 'sclkd', 'lmst', 'ltst']
ALLOWED_OUTPUT_TYPES = ['scet', 'utc', 'ert', 'ett', 'gps', 'pt', 'pst', 'pdt', 'isoc',
                        'et', 'sclk', 'sclkd', 'lmst', 'ltst', 'upleg', 'downleg', 'rtlt']
SPICE_IMPORTED = False

# this map will be filled during SCLKD conversions
SCLK_FRACTIONAL_PART_TO_SCID_DICT = {}

# this map will be used for LTST conversions and error checks
# basically we want to compare to sol 0 but we don't want to recompute it every time
LMST_EPOCH_TO_SCID_DICT = {}


class JplTimeError(ValueError):
    pass

class DurationError(JplTimeError):
    pass

class DurationFormatError(DurationError):
    pass

class TimeError(JplTimeError):
    pass

class TimeFormatError(TimeError):
    pass

class TimeConversionError(TimeError):
    pass

class EpochRelativeTimeError(TimeError):
    pass

class EpochRelativeTimeFormatError(EpochRelativeTimeError):
    pass

class KernelError(TimeError):
    pass

class KernelMissingError(KernelError):
    pass

def parse_spice_error(spice_error):
    """
    Parses a Spiceypy error message to throw a more specific exception.
    :param spice_error: spiceypy.stypes.SpiceyError
    :return:
    """
    if 'MISSINGTIMEINFO' in str(spice_error):
        raise KernelMissingError(spice_error)

    elif 'INVALIDTIMESTRING' in str(spice_error):
        raise TimeFormatError(spice_error)

    else:
        raise TimeConversionError(spice_error)


class Duration(object):
    """Used to perform duration math, format durations, convert from Earth
    to Mars durations, and perform math with Time objects."""

    # precision for methods comparing durations and for output
    # duration epsilon is what is actually used for any comparisons, and
    # is slightly less than the precision because of floating point error
    DURATION_DECIMAL_PRECISION = 3
    DURATION_EPSILON = .000999

    def __init__(self, duration_of_unknown_type=0):
        """
        :param duration_of_unknown_type: duration string, int, float, timedelta, or duration
        :type duration_of_unknown_type: object
        """
        self.seconds = Duration.__convert_object_to_seconds(duration_of_unknown_type)

    def __add__(self, duration_or_time):
        if isinstance(duration_or_time, Time) or isinstance(duration_or_time, EpochRelativeTime):
            return duration_or_time + self
        else:
            return Duration(self.seconds + Duration(duration_or_time).seconds)

    def __sub__(self, other_duration):
        return Duration(self.seconds - other_duration.seconds)

    def __mul__(self, coeff):
        # we should only be multiplying by floats or ints
        return Duration(self.seconds * coeff)

    def __div__(self, coeff):
        # if dividing by an int or float then return a Duration
        if isinstance(coeff, (int, float)):
            return Duration(self.seconds / coeff)

        # otherwise, assume it represents a duration and return a float
        else:
            return self.seconds / Duration(coeff).to_seconds()

    def __truediv__(self, coeff):
        # if dividing by an int or float then return a Duration
        if isinstance(coeff, (int, float)):
            return Duration(self.seconds / coeff)

        # otherwise, assume it represents a duration and return a float
        else:
            return self.seconds / Duration(coeff).to_seconds()

    def __eq__(self, other_duration):
        if other_duration and isinstance(other_duration, Duration):
            return abs(self.seconds - other_duration.seconds) < Duration.DURATION_EPSILON
        else:
            return False

    def __ne__(self, other_duration):
        if other_duration and isinstance(other_duration, Duration):
            return abs(self.seconds - other_duration.seconds) >= Duration.DURATION_EPSILON
        else:
            return True

    def __lt__(self, other_duration):
        return self.seconds + Duration.DURATION_EPSILON < other_duration.seconds

    def __le__(self, other_duration):
        return self < other_duration or self == other_duration

    def __gt__(self, other_duration):
        return self.seconds > other_duration.seconds + Duration.DURATION_EPSILON

    def __ge__(self, other_duration):
        return self > other_duration or self == other_duration

    def __mod__(self, duration_int_or_float):
        if isinstance(duration_int_or_float, Duration):
            # we want to operate with integers and not floats for modulus to get intuitive behavior
            # the min precision supported by Duration is microseconds
            microseconds = int(round(self.to_seconds() * 10**6))
            input_microseconds = int(round(duration_int_or_float.to_seconds() * 10**6))
            result_microseconds = microseconds % input_microseconds
            return Duration(result_microseconds / 10**6)

        else:
            raise DurationError('Error, can only call % with a Duration and another Duration')

    def __repr__(self):
        return self.to_string()

    def to_timedelta(self):
        """
        Returns the duration object as a timedelta.

        :return: timedelta representing duration
        :rtype: timedelta
        """
        return timedelta(seconds=self.seconds)

    def to_string(self, num_decimals=None):
        """
        Returns a string representation of the duration object.

        :param num_decimals: number of decimals to output in the string
        :type num_decimals: int
        :return: duration string
        :rtype: str
        """

        # get correct number of decimals to use
        updated_num_decimals = Duration.get_duration_decimal_precision(num_decimals)

        # round total seconds to 6 decimal places
        total_seconds = round(self.seconds, updated_num_decimals)

        # calculate hours, min, sec
        days, remainder = divmod(abs(total_seconds), time_globals.SECONDS_PER_DAY)
        hours, remainder = divmod(remainder, time_globals.SECONDS_PER_HOUR)
        minutes, seconds = divmod(remainder, time_globals.SECONDS_PER_MINUTE)

        if total_seconds < 0:
            sign = '-'
        else:
            sign = ''

        day_timestamp = '{:1.0f}T'.format(days) if days > 0 else ''

        if updated_num_decimals > 0:
            seconds_length = 3 + updated_num_decimals
            timestamp = '{}{}{:02.0f}:{:02.0f}:{:0{}.{}f}'.format(
                sign, day_timestamp, hours, minutes, seconds, seconds_length, updated_num_decimals)

        else:
            timestamp = '{}{}{:02.0f}:{:02.0f}:{:02.0f}'.format(
                sign, day_timestamp, hours, minutes, seconds)

        return timestamp

    def to_seconds(self):
        """
        Returns the total number of seconds in the duration as a float.

        :return: number of seconds
        :rtype: float
        """
        return self.seconds

    def to_minutes(self):
        """
        Return the total number of minutes as a float.
        :return: float number of minutes
        :rtype: float
        """
        return self.seconds / 60

    def to_hours(self):
        """
        Return the total number of hours as a float.
        :return: float number of hours
        :rtype: float
        """
        return self.seconds / (60 * 60)

    def to_days(self):
        """
        Return the total number of days as a float.
        :return: float number of days
        :rtype: float
        """
        return self.seconds / (60 * 60 * 24)

    def to_mars_dur(self, num_decimals=None):
        """
        Converts the duration object to a string representing the duration
        as a mars duration.

        :return: mars duration string
        :rtype: str
        """
        # get correct number of decimals to use
        updated_num_decimals = Duration.get_duration_decimal_precision(num_decimals)

        lmst_total_seconds = round(abs(self.seconds / time_globals.MARS_TIME_SCALE), updated_num_decimals)

        sols, remainder = divmod(lmst_total_seconds, time_globals.SECONDS_PER_DAY)
        hours, remainder = divmod(remainder, time_globals.SECONDS_PER_HOUR)
        minutes, seconds = divmod(remainder, time_globals.SECONDS_PER_MINUTE)

        if self.seconds < 0:
            sign = '-'
        else:
            sign = ''

        if sols > 0:
            pre_seconds_string = '{}{:1.0f}M{:02.0f}:{:02.0f}:'.format(sign, sols, hours, minutes)
        else:
            pre_seconds_string = '{}M{:02.0f}:{:02.0f}:'.format(sign, hours, minutes)

        if updated_num_decimals > 0:
            seconds_length = 3 + updated_num_decimals
            return pre_seconds_string + '{:0{}.{}f}'.format(seconds, seconds_length, updated_num_decimals)
        else:
            return pre_seconds_string + '{:02.0f}'.format(seconds)

    def strfdelta(self, format_string):
        """
        Returns the Duration formatted based on the input format string.
        Input format string should match the standard python {} .format, with
        {0} = sign
        {1} = days
        {2} = hours
        {3} = minutes
        {4} = seconds (float)
        Example:
        d.strfdelta('{1:02d}T{2:02d}:{3:02d}:{4:06.3f}') = 03T04:05:06.789
        d.strfdelta('{0}{1} days,{2} hours, :{3} minutes, :{4} seconds') = -3 days, 4 hours, 5 minutes, 6.789 seconds

        :param format_string: python .format string for integers
        :type format_string: str
        :return: mars duration string
        :rtype: str
        """
        regex_match = re.search(time_globals.DURATION_EXACT_REGEX, self.to_string(6))

        sign = regex_match.group('sign') if regex_match.group('sign') else ''
        days = int(regex_match.group('days')) if regex_match.group('days') else 0
        hours = int(regex_match.group('hours'))
        minutes = int(regex_match.group('minutes'))
        seconds = float(regex_match.group('seconds') + '.' + regex_match.group('decimal'))

        return format_string.format(sign, days, hours, minutes, seconds)

    def mars_strfdelta(self, format_string):
        """
        Returns the Duration formatted based on the input format string as a Mars duration.
        Input format string should match the standard python {} .format, with
        {0} = sign
        {1} = sols
        {2} = mars hours
        {3} = mars minutes
        {4} = mars seconds (float)
        Example:
        d.mars_strfdelta('{0}{1:04d}M{2:02d}:{3:02d}:{4:06.3f}') = -003M04:05:06.789
        d.mars_strfdelta('{0}{1} sols,{2} hours,{3} minutes,{4} seconds') = -3 sols, 4 hours, 5 minutes, 6.789 seconds

        :param format_string: python .format string for integers
        :type format_string: str
        :return: mars duration string
        :rtype: str
        """
        regex_match = re.search(time_globals.MARS_DURATION_EXACT_REGEX, self.to_mars_dur(6))

        sign = regex_match.group('sign') if regex_match.group('sign') else ''
        sol_number = int(regex_match.group('sols')) if regex_match.group('sols') else 0
        hours = int(regex_match.group('hours'))
        minutes = int(regex_match.group('minutes'))
        seconds = float(regex_match.group('seconds') + '.' + regex_match.group('decimal'))

        return format_string.format(sign, sol_number, hours, minutes, seconds)

    def abs(self):
        """
        Returns the absolute value of the duration as a duration object.

        :return: absolute value of duration
        :rtype: Duration
        """
        return Duration(abs(self.seconds))

    def round(self, resolution_duration):
        """
        Returns the duration object rounded to the input resolution.

        :param resolution_duration: resolution for rounding
        :type resolution_duration: Duration
        :return: rounded duration
        :rtype: Duration
        """
        scale = round(self.seconds / resolution_duration.seconds)
        return Duration(scale * resolution_duration.seconds)

    def ceil(self, resolution_duration):
        """
        Returns the duration object rounded up to the input resolution.

        :param resolution_duration: resolution for rounding
        :type resolution_duration: Duration
        :return: rounded up duration
        :rtype: Duration
        """
        scale = math.ceil(self.seconds / resolution_duration.seconds)
        return Duration(scale * resolution_duration.seconds)

    def floor(self, resolution_duration):
        """
        Returns the duration object rounded down to the input resolution.

        :param resolution_duration: resolution for rounding
        :type resolution_duration: Duration
        :return: rounded down duration
        :rtype: Duration
        """
        scale = math.floor(self.seconds / resolution_duration.seconds)
        return Duration(scale * resolution_duration.seconds)

    @staticmethod
    def set_comparison_precision(seconds):
        """
        Updates the default DURATION_EPSILON used for comparing durations.
        Default comparison precision is .001 seconds (1 ms).

        :param seconds: precision to use as seconds or fractions of a second
        :type seconds: float
        :return: None
        """
        # subtract off a small amount to account for floating point error
        # we should never need to subtract off more than a second
        Duration.DURATION_EPSILON = seconds - min(seconds/1000, 1)

    @staticmethod
    def set_output_decimal_precision(precision):
        """
        Updates the default DURATION_DECIMAL_PRECISION
        :param precision: new decimal precision
        :type precision: int
        :return: None
        """
        Duration.DURATION_DECIMAL_PRECISION = precision

    @staticmethod
    def get_duration_decimal_precision(override_duration_decimal_precision=None):
        """
        Returns the duration decimal precision, but allows users to pass a value to override
        the value it would otherwise return. This is needed specifically for the
        methods which want to get the new default duration decimal precision.

        :param override_duration_decimal_precision: non-default precision to use
        :type override_duration_decimal_precision: int
        :return: duration decimal precision
        :rtype: int
        """
        if isinstance(override_duration_decimal_precision, int):
            return override_duration_decimal_precision

        return Duration.DURATION_DECIMAL_PRECISION

    @staticmethod
    def __convert_object_to_seconds(duration_of_unknown_type):
        """
        Converts an unknown object representing a duration into a number
        of seconds. Allowable types are timedeltas, Durations, floats,
        earth duration strings, and mars duration strings. Only expected
        to be used within Duration.

        :param duration_of_unknown_type: object representing a duration
        :type duration_of_unknown_type: object
        :return: Duration object
        :rtype: float
        """
        # if this is a timedelta then we can just conver to seconds
        if isinstance(duration_of_unknown_type, timedelta):
            return duration_of_unknown_type.total_seconds()

        # if this is a string then we need to check the format
        elif isinstance(duration_of_unknown_type, str):
            scrubbed_string = duration_of_unknown_type.strip()

            # if empty string, return 0
            if scrubbed_string == '':
                return 0

            # if this matches the standard duration regex then assume earth time
            if time_globals.DURATION_EXACT_REGEX.match(scrubbed_string):
                return Duration.__earth_dur_string_to_seconds(scrubbed_string)

            # if the duration matches the mars regex (contains an M before the duration)
            # then convert it to earth seconds
            elif time_globals.MARS_DURATION_EXACT_REGEX.match(scrubbed_string):
                return Duration.__mars_dur_string_to_seconds(scrubbed_string)

            else:
                raise DurationFormatError('String value passed to Duration constructor must match either '
                                 'the earth or mars duration regex, or be an empty string, but the '
                                 'input value was {}.'.format(str(duration_of_unknown_type)))

        # if this is a float or int then assume it is a number of seconds
        elif isinstance(duration_of_unknown_type, (int, float)):
            return float(duration_of_unknown_type)

        # if this is a duration object then just return the seconds
        elif isinstance(duration_of_unknown_type, Duration):
            return duration_of_unknown_type.to_seconds()

        elif duration_of_unknown_type == None:
            return 0

        # try casting to string to work for unicode in python2
        else:
            try:
                return Duration.__convert_object_to_seconds(str(duration_of_unknown_type))
            except:
                # if we haven't returned yet then raise error
                raise DurationFormatError("Value passed to Duration constructor must be a "
                                 "timedelta object, Earth or Mars duration string, "
                                 "or a number of earth seconds. Received: {}".format(
                                 duration_of_unknown_type))

    @staticmethod
    def __mars_dur_string_to_seconds(mars_dur):
        """
        Converts a mars duration to an earth duration.
        The only difference in the regex is an M instead of a T, so this function replaces
        the M with a T and then gets the total seconds assuming it is utc. It then returns
        the seconds multiplied by the time scale to get the correct duration. Only expected
        to be used from Duration.

        :param mars_dur: mars duration string
        :type mars_dur: str
        :return: earth seconds
        :rtype: float
        """
        regex_match = time_globals.MARS_DURATION_REGEX.match(mars_dur)

        if regex_match:
            mars_seconds = Duration.__earth_dur_string_to_seconds(mars_dur.replace('M', 'T'))
            return mars_seconds * time_globals.MARS_TIME_SCALE

        else:
            raise DurationFormatError("Mars duration {} as passed to mars_dur_string_to_seconds "
                             "is not valid".format(mars_dur))

    @staticmethod
    def __earth_dur_string_to_seconds(earth_dur):
        """This function takes in a timestamp string and returns a number of
        seconds as a float. Only expected to be used internal to Duration.

        :param earth_dur: duration string
        :type earth_dur: str
        :return: total seconds
        :rtype: float
        """

        regex_match = re.search(time_globals.DURATION_REGEX, earth_dur)
        if regex_match:
            if regex_match.group('days'):
                days = int(regex_match.group('days'))
            else:
                days = 0

            hours = int(regex_match.group('hours'))
            minutes = int(regex_match.group('minutes'))
            seconds = float(regex_match.group('full_seconds'))  # full_seconds includes decimal

            # calculate total seconds in duration
            total_seconds = days * time_globals.SECONDS_PER_DAY + \
                            hours * time_globals.SECONDS_PER_HOUR + \
                            minutes * time_globals.SECONDS_PER_MINUTE + \
                            seconds

            if regex_match.group('sign'): total_seconds = total_seconds * -1

            return float(total_seconds)

        # give error if timestamp does not match expected regex
        else:
            raise DurationFormatError("Error - malformed Earth duration {} given to "
                             "earth_dur_string_to_seconds. ".format(earth_dur))


class Time(object):
    """Used to perform time calculations such as UTC to LMST, SCET to ERT, etc.
    and for performing operations between times and durations."""

    # static variables - these are default values, update with static methods
    SPACECRAFT_ID = None
    LMST_SCLK_ID = None
    LMST_FRACTIONAL_PART = 100000 # fractional part of LMST for conversions to ET
    COMPARISON_PRECISION = Duration("00:00:00.000999") # default to 1 ms - 1 us
    OUTPUT_DECIMAL_PRECISION = 3 # default to 3 decimal places
    GST_SECONDS_PER_SOL = 88775

    def __init__(self, time_of_unknown_type=0):
        """Takes in a string, time object or number of seconds since the epoch to 
        create a time object. The time object is tracked by seconds as a float under 
        the hood, and uses spiceypy to convert to/from SCET, LMST, LTST, etc.

        :param time_of_unknown_type: time string, datetime, or ephemeris time seconds since J2000
        :type time_of_unknown_type: object
        """
        self.et = Time.__calculate_et(time_of_unknown_type)
        self.tai = None

    def __add__(self, duration):
        return Time(Time.tai2et(self.to_tai() + duration.to_seconds()))

    def __sub__(self, duration_or_time):
        # Subtract two times to get a duration
        if isinstance(duration_or_time, Time):
            return Duration(self.to_tai() - duration_or_time.to_tai())
        else:
            return Time(Time.tai2et(self.to_tai() - duration_or_time.to_seconds()))

    def __eq__(self, other_time):
        if other_time and isinstance(other_time, Time):
            return abs(self.to_tai() - other_time.to_tai()) < Time.COMPARISON_PRECISION.seconds
        else:
            return False

    def __ne__(self, other_time):
        if other_time and isinstance(other_time, Time):
            return abs(self.to_tai() - other_time.to_tai()) >= Time.COMPARISON_PRECISION.seconds
        else:
            return True

    def __lt__(self, other_time):
        return self.to_tai() + Time.COMPARISON_PRECISION.seconds < other_time.to_tai()

    def __le__(self, other_time):
        return self < other_time or self == other_time

    def __gt__(self, other_time):
        return self.to_tai() > other_time.to_tai() + Time.COMPARISON_PRECISION.seconds

    def __ge__(self, other_time):
        return self > other_time or self == other_time

    def __repr__(self):
        return self.to_utc()

    def is_between(self, start, end):
        """
        Returns true if the time is greater than or equal to the start and
        less than or equal to the end, and false if not.

        :param start: start time of window
        :type start: Time
        :param end: end time of window
        :type end: Time
        :return: true if within window, false if not
        :rtype: bool
        """
        if start > end:
            raise TimeError('Error calling is_between on time {}. Input start time {} '
                            'is greater than end time {}'.format(self.to_utc(), start.to_utc(), end.to_utc()))

        return start < self < end

    def round(self, resolution_duration, reference_time=None):
        """
        Returns a new time object rounded to the input resolution.

        :param resolution_duration: resolution used for rounding
        :type resolution_duration: Duration
        :param reference_time: reference to use for rounding
        :type reference_time: Time
        :return: rounded time object
        :rtype: Time
        """
        if not reference_time:
            reference_time = Time.__get_year_time(self)
        difference_duration = self - reference_time
        difference_duration = difference_duration.round(resolution_duration)
        return reference_time + difference_duration

    def ceil(self, resolution_duration, reference_time=None):
        """
        Returns a new time object rounded up to the input resolution.

        :param resolution_duration: resolution used for rounding
        :type resolution_duration: Duration
        :param reference_time: reference to use for rounding
        :type reference_time: Time
        :return: rounded up time object
        :rtype: Time
        """
        if not reference_time:
            reference_time = Time.__get_year_time(self)
        difference_duration = self - reference_time
        return reference_time + difference_duration.ceil(resolution_duration)

    def floor(self, resolution_duration, reference_time=None):
        """
        Returns a new time object rounded down to the input resolution.

        :param resolution_duration: resolution used for rounding
        :type resolution_duration: Duration
        :param reference_time: reference to use for rounding
        :type reference_time: Time
        :return: rounded down time object
        :rtype: Time
        """
        if not reference_time:
            reference_time = Time.__get_year_time(self)
        difference_duration = self - reference_time
        return reference_time + difference_duration.floor(resolution_duration)

    def round_lmst(self, resolution_mars_duration, reference_time=None):
        """
        Takes in a mars duration (as a duration object) and rounds an LMST time
        appropriately. Behaves like round(), but on the LMST time.

        :param resolution_mars_duration: resolution used for rounding, best to use a mars duration, e.g. M02:00:00
        :type resolution_mars_duration: Duration
        :param reference_time: reference to use for rounding
        :type reference_time: Time
        :return: rounded time object
        :rtype: Time
        """
        if not reference_time:
            reference_time = Time('Sol-{}M00:00:00'.format(self.to_sols()))
        return self.round(resolution_mars_duration, reference_time)

    def ceil_lmst(self, resolution_mars_duration, reference_time=None):
        """
        Takes in a mars duration (as a duration object) and ceils an LMST time
        appropriately. Behaves like ceil(), but on the LMST time.

        :param resolution_mars_duration: resolution used for rounding, best to use a mars duration, e.g. M02:00:00
        :type resolution_mars_duration: Duration
        :param reference_time: reference to use for rounding
        :type reference_time: Time
        :return: rounded time object
        :rtype: Time
        """
        if not reference_time:
            reference_time = Time('Sol-{}M00:00:00'.format(self.to_sols()))
        return self.ceil(resolution_mars_duration, reference_time)

    def floor_lmst(self, resolution_mars_duration, reference_time=None):
        """
        Takes in a mars duration (as a duration object) and floors an LMST time
        appropriately. Behaves like floor(), but on the LMST time.

        :param resolution_mars_duration: resolution used for rounding, best to use a mars duration, e.g. M02:00:00
        :type resolution_mars_duration: Duration
        :param reference_time: reference to use for rounding
        :type reference_time: Time
        :return: rounded time object
        :rtype: Time
        """
        if not reference_time:
            reference_time = Time('Sol-{}M00:00:00'.format(self.to_sols()))
        return self.floor(resolution_mars_duration, reference_time)

    def to_string(self, precision=None, format_type='ISOD'):
        return self.__to_utc_format__(precision, format_type)

    def __to_utc_format__(self, precision=None, format_type='ISOD'):
        """
        Returns a string representation of the time object in SCET.

        :param precision: decimal precision of time string
        :type precision: int
        :param format_type: string name of format type for SPICE
        :type format_type: str
        :return: string representation of SCET time
        :rtype: str
        """
        try:
            return spice.et2utc(self.et,
                                format_type,
                                Time.get_time_output_precision(precision),
                                time_globals.MAX_OUTPUT_LENGTH)
        except spice.stypes.SpiceyError as e:
            parse_spice_error(e)

    def to_utc(self, precision=None):
        """
        Returns a string representation of the time object in SCET with ISOD format.

        :param precision: decimal precision of time string
        :type precision: int
        :return: string representation of SCET time
        :rtype: str
        """
        return self.__to_utc_format__(Time.get_time_output_precision(precision), 'ISOD')

    def to_isoc(self, precision=None):
        """
        Returns a string representation of the time object in SCET with ISOC format.

        :param precision: decimal precision of time string
        :type precision: int
        :return: string representation of SCET time
        :rtype: str
        """
        return self.__to_utc_format__(Time.get_time_output_precision(precision), 'ISOC')

    def to_julian(self, precision=None):
        """
        Returns a string representation of the time object in SCET with julian format.

        :param precision: decimal precision of time string
        :type precision: int
        :return: string representation of SCET time
        :rtype: str
        """
        return self.__to_utc_format__(Time.get_time_output_precision(precision), 'J')

    def to_calendar(self, precision=None):
        """
        Returns a string representation of the time object in SCET with calendar format.

        :param precision: decimal precision of time string
        :type precision: int
        :return: string representation of SCET time
        :rtype: str
        """
        return self.__to_utc_format__(Time.get_time_output_precision(precision), 'C')

    def to_lmst(self, precision=None, lmst_sclk_id=None):
        """
        Converts the time object to LMST and returns it as a string.

        :param precision: number of digits for output LMST string
        :type precision: int
        :param lmst_sclk_id: ID of SCLK kernel for LMST conversion
        :type lmst_sclk_id: int
        :return: string representation of LMST time
        :rtype: str
        """
        try:
            return Time.__reformat_spice_lmst(
                spice.sce2s(Time.get_lmst_sclk_id(lmst_sclk_id),
                            self.et,
                            time_globals.MAX_OUTPUT_LENGTH),
                Time.get_time_output_precision(precision))

        # if we are unable to convert to LMST then let's make sure that it isn't
        # due to the time being before sol 0
        except spice.stypes.SpiceyError as e:
            sol_0_time = Time.get_lmst_epoch(lmst_sclk_id)
            if self < sol_0_time:
                raise TimeConversionError('Error converting {} to LMST. Time is before the LMST '
                                 'epoch: {}'.format(
                    self.to_utc(), sol_0_time.to_utc()
                ))
            else:
                raise TimeConversionError(e)

    def to_lmst_am_pm(self, lmst_sclk_id=None):
        """
        Returns 'PM' if to_lmst() has time of day >= 12:00:00
        and 'AM' otherwise.
        :param lmst_sclk_id: sclk id for LMST (spacecraft id followed by 900 usually)
        :type lmst_sclk_id: int
        :return: 'AM' or 'PM'
        :rtype: str
        """
        lmst_hours = int(self.to_lmst_strftime('{1}', lmst_sclk_id))
        if lmst_hours >= 12:
            return 'PM'
        else:
            return 'AM'

    def to_ltst(self, spacecraft_id=None):
        """
        Converts the time object to LTST and returns it as a string.
        Calculates the Mars longitude using the landed SPK and then
        uses SPICE to calculate local solar time.

        :param spacecraft_id: spacecraft NAIF ID
        :type spacecraft_id: int
        :return: string representation of LTST time
        :rtype: str
        """
        longitude_rad = Time.__calculate_mars_longitude(self.et, Time.get_spacecraft_id(spacecraft_id))
        try:
            ltst_hr, ltst_min, ltst_sec, _, _ = spice.et2lst(
                self.et,
                time_globals.MARS_NAIF_ID,
                longitude_rad,
                'PLANETOCENTRIC',
                time_globals.MAX_OUTPUT_LENGTH,
                time_globals.MAX_OUTPUT_LENGTH)

            return Time.__reformat_spice_ltst(
                self.to_lmst(),
                ltst_hr,
                ltst_min,
                ltst_sec)

        except spice.stypes.SpiceyError as e:
            parse_spice_error(e)

    def to_sclk(self, spacecraft_id=None):
        """
        Returns a representation of the time object as a SCLK string for the input
        spacecraft.

        :param spacecraft_id: naif id of spacecraft
        :type spacecraft_id: int
        :return: string representation of SCLK time
        :rtype: str
        """
        try:
            return spice.sce2s(Time.get_spacecraft_id(spacecraft_id), self.et)

        except spice.stypes.SpiceyError as e:
            parse_spice_error(e)

    def to_sclkd(self, spacecraft_id=None):
        """
        Returns a representation of the time object as a SCLK decimal float.

        :param spacecraft_id: naif id of spacecraft
        :type spacecraft_id: int
        :return: float representing SCLK time
        :rtype: float
        """
        try:
            sclk_string = spice.sce2s(Time.get_spacecraft_id(spacecraft_id), self.et)

        except spice.stypes.SpiceyError as e:
            parse_spice_error(e)

        regex_match = re.search(time_globals.SCLK_REGEX_EXACT, sclk_string)
        if regex_match:
            subseconds = int(regex_match.group('fraction')) / float(Time.get_sclk_fractional_part(spacecraft_id))
            return int(regex_match.group('seconds')) + subseconds
        else:
            raise TimeConversionError('Error converting {} into SCLKD value.'.format(self.to_utc()))

    def to_gst(self, last_local_midnight_time, spacecraft_id=None):
        """
        Converts the time object to a GST (generic sol time) integer value.
        GST is calculated by taking the difference in the SCLK values of the
        current time and the last_local_midnight_time and then taking the modulus
        of that value and 88775 (approx number of seconds in a mars day).
        :param last_local_midnight_time: Time of the last local midnight parameter update
        :type last_local_midnight_time: Time
        :type spacecraft_id: int
        :return: GST integer, SCLK seconds from the calculated local midnight
        :rtype: int
        """
        return int(round((self.to_sclkd(spacecraft_id=spacecraft_id) - last_local_midnight_time.to_sclkd(spacecraft_id=spacecraft_id)) % Time.GST_SECONDS_PER_SOL))

    def to_sols(self):
        """
        Returns the current LMST sol number.

        :return: LMST sol number
        :rtype: int
        """
        return int(time_globals.LMST_REGEX.match(self.to_lmst()).group('sol'))

    def to_fractional_sols(self):
        """
        Returns the sol number as a float, which has a decimal representing the
        time in LMST as a fraction of a Mars day.

        :return: LMST as a fractional sol number
        :rtype: float
        """
        lmst_time_of_day = time_globals.LMST_REGEX.match(
            self.to_lmst()).group('time_of_day')

        return self.to_sols() + Time.__time_of_day_to_fractional_day(
                   Duration(lmst_time_of_day))

    def to_et(self):
        """
        Returns the Ephemeris Time seconds since J2000.

        :return: ET seconds
        :rtype: float
        """
        return self.et

    def to_tai(self):
        """
        Returns TAI seconds as a float.

        :return: TAI seconds
        :rtype: float
        """
        if not self.tai:
            self.tai = Time.et2tai(self.et)

        return self.tai

    def to_gps(self, precision=None):
        """
        Returns the GPS time as a string in the UTC format.
        Note: SPICE does not support GPST, so we need to calculate it
        ourselves. The method is as follows:
        The two special cases for GPS time are:
        1) Epoch = 1980-006T00:00:00.000
        2) GPS time does not account for leap seconds

        We can take advantage of the fact that Python datetime does not
        account for leap seconds to compute the GPS time:
        1) compute TAI at 1980-006T00:00:00 (this is GPS = 0.0)
        2) store offset from TAI to GPS epochs
        3) use offset to get GPS seconds (returns seconds)
        4) use python datetime to add a timedelta from 1980-006T00:00:00
        5) return new datetime output as a string (returns GPST time string)

        :param precision: decimal precision of time string
        :type precision: int
        :return: GPS time as a string
        :rtype: str
        """
        gps_timedelta = timedelta(seconds=self.to_gps_seconds())
        gps_epoch_dt = datetime(1980, 1, 6)

        # this will give us the right output, even though it looks weird
        return Time(gps_epoch_dt + gps_timedelta).__to_utc_format__(precision)

    def to_gps_seconds(self):
        """
        Returns GPS seconds as a float.
        Note: SPICE does not support GPST, so we need to calculate it
        ourselves. See comment in to_gps.

        :return: GPS seconds
        :rtype: float
        """
        tai_at_gps_epoch = Time(GPST_EPOCH).to_tai() # this will be a large negative number of seconds
        return self.to_tai() - tai_at_gps_epoch # add the seconds to the current TAI

    def to_scet(self, precision=None):
        """
        Returns SCET time as UTC formatted string.
        :param precision: decimal precision of time string
        :type precision: int
        :return: SCET time string
        :rtype: str
        """
        return self.to_utc(precision=precision)

    def to_ert(self, spacecraft_id=None, body_id=time_globals.EARTH_NAIF_ID):
        """
        Returns the time object converted to earth received time as a
        UTC string. ERT is calculated by adding downleg to the SCET time.

        :param spacecraft_id: id of spacecraft for OWLT calculation
        :type spacecraft_id: int
        :param body_id: id of body for OWLT calculation
        :type body_id: int
        :return: UTC string of time converted to ERT
        :rtype: str
        """
        return (self + Time.downleg(self, 'SCET', spacecraft_id, body_id)).to_utc()

    def to_ett(self, spacecraft_id=None, body_id=time_globals.EARTH_NAIF_ID):
        """
        Returns the time object converted to earth transmit time as a
        UTC string. ETT is calculated by subtracting upleg from the SCET time.

        :param spacecraft_id: id of spacecraft for OWLT calculation
        :type spacecraft_id: int
        :param body_id: id of body for OWLT calculation
        :type body_id: int
        :return: UTC string of time converted to ETT
        :rtype: str
        """
        return (self - Time.upleg(self, 'SCET', spacecraft_id, body_id)).to_utc()

    def to_datetime(self):
        """
        Returns a datetime object representing the UTC time object.
        If the time is on a leap second then the datetime object returned will be 1 second
        before the leap second.
        :return: datetime object from utc string
        :rtype: datetime
        """
        try:
            return Time.__utc_to_datetime(self.to_utc())
        # if we are at a leap second then the time looks like 2016-366T23:59:60, so we need to subtract
        # a second so datetime doesn't explode
        except ValueError:
            return Time.__utc_to_datetime((self - Duration(1)).to_utc())

    def to_date(self):
        """
        Returns the time object as a datetime.date object.
        :rtype: date
        """
        return self.to_datetime().date()

    def to_pt(self):
        """
        Returns a string representation of the time object in the America/Los_Angeles
        time zone.

        :return: UTC string of time in America/Los_Angeles time zone
        :rtype: str
        """
        return self.to_timezone(PACIFIC_TIME_ZONE)

    def to_pst(self):
        """
        Returns a string representation of the time object in the GMT-8
        time zone.

        :return: UTC string of time in PST time zone
        :rtype: str
        """
        return self.to_timezone(PST_TIME_ZONE)

    def to_pdt(self):
        """
        Returns a string representation of the time object in the GMT-7
        time zone.

        :return: UTC string of time in PDT time zone
        :rtype: str
        """
        return self.to_timezone(PDT_TIME_ZONE)

    def to_indian_std_time(self):
        """
        Returns a string representation of the time object in the America/Los_Angeles
        time zone.

        :return: UTC string of time in Asia/Kolkata time zone
        :rtype: str
        """
        return self.to_timezone(ISRO_TIME_ZONE)

    def to_timezone(self, timezone_name):
        """
        Returns a string representation of the time object in the input time zone.

        :param timezone_name: string name of timezone, compatible with pytz
        :type timezone_name: str
        :return: UTC string of time in input time zone
        """
        offset = Time.__get_timezone_offset(self, timezone_name)
        return (self + offset).__to_utc_format__()

    def to_utc_strftime(self, time_format_string):
        """
        Returns the UTC time as a string with the input format. Uses the
        datetime strftime format string.

        :param time_format_string: string time format from datetime
        :type time_format_string: str
        :return: string representing utc time
        :rtype: str
        """
        return self.to_datetime().strftime(time_format_string)

    def to_lmst_strftime(self, time_format_string, lmst_sclk_id=None):
        """
        Returns the LMST time formatted based on the input time string.
        Input time string should match the standard python {} .format, with
        {0} = sol number
        {1} = hours
        {2} = minutes
        {3} = seconds (float)
        Example:
        t.to_lmst_strftime('Sol-{0:04d}M{1:02d}:{2:02d}:{3:06.3f}') = Sol-0003M04:05:06.789
        t.to_lmst_strftime('SOL {0:04d} {1:02d}:{2:02d}:{3:09.6f}') = SOL 0003 04:05:06.789000

        :param time_format_string: python .format string for integers
        :type time_format_string: str
        :return: LMST time string
        :rtype: str
        """
        regex_match = re.search(time_globals.LMST_EXACT_REGEX, self.to_lmst(6, lmst_sclk_id))
        sol_number = int(regex_match.group('sol'))
        hours = int(regex_match.group('hours'))
        minutes = int(regex_match.group('minutes'))
        seconds = float(regex_match.group('seconds') + '.' + regex_match.group('decimal'))

        return time_format_string.format(sol_number, hours, minutes, seconds)

    @staticmethod
    def set_spacecraft_id(spacecraft_id):
        """
        Updates the default SPACECRAFT_ID static variable.

        :param spacecraft_id: NAIF ID of spacecraft
        :type spacecraft_id: int
        :return: None
        """
        Time.SPACECRAFT_ID = spacecraft_id

    @staticmethod
    def set_lmst_sclk_id(lmst_sclk_id):
        """
        Updates the default LMST_SCLK_ID static variable, which is used
        for LMST conversions.

        :param lmst_sclk_id: NAIF LMST SCLK ID for spacecraft
        :type lmst_sclk_id: int
        :return: None
        """
        Time.LMST_SCLK_ID = lmst_sclk_id

    @staticmethod
    def set_spacecraft_id_and_lmst_id(spacecraft_id):
        """
        Sets the spacecraft ID and sets the LMST SCLK ID to the
        spacecraft id followed by 900.
        :param spacecraft_id: NAIF ID of spacecraft
        :type spacecraft_id: int
        :return: None
        """
        Time.SPACECRAFT_ID = spacecraft_id
        Time.LMST_SCLK_ID = int(str(spacecraft_id) + '900')

    @staticmethod
    def set_comparison_precision(precision):
        """
        Updates the default time precision used for comparisons.

        :param precision: duration precision to use
        :type precision: Duration
        :return: None
        """
        # subtract off a small amount to account for floating point error
        # we should never need to subtract more than 1 second
        Time.COMPARISON_PRECISION = precision - min([precision/1000, Duration(1)])

    @staticmethod
    def set_output_decimal_precision(precision):
        """
        Sets the default output precision to use for strings.

        :param precision: number of decimals for output, can be negative
        :type precision: int
        :return: None
        """
        Time.OUTPUT_DECIMAL_PRECISION = precision

    @staticmethod
    def set_lmst_fractional_part(lmst_fractional_part):
        """
        Sets the integer SCLK fractional part value, which is used to convert
        from SCLK to SCLKD and vice-versa.

        :param lmst_fractional_part: count of fractions of a second in SCLK value
        :type lmst_fractional_part: int
        :return: None
        """
        Time.LMST_FRACTIONAL_PART = lmst_fractional_part

    @staticmethod
    def owlt(et, target_id, direction, observer_id):
        """
        Calculates and returns the OWLT from the target id to the observer id.
        :param et: ephemeris time seconds since J2000
        :type et: float
        :param target_id: naif id of target spacecraft or body
        :type target_id: int
        :param direction: either '->' or '<-' for the ltime spice call
        :type direction: str
        :param observer_id: naif id of observer spacecraft or body
        :type observer_id: int
        :return: one way light time as a duration object
        :rtype: Duration
        """
        try:
            return Duration(spice.ltime(et, target_id, direction, observer_id)[1])

        except spice.stypes.SpiceyError as e:
            parse_spice_error(e)

    @staticmethod
    def rtlt(time, time_reference='SCET', spacecraft_id=None, body_id=time_globals.EARTH_NAIF_ID):
        """
        Takes in a time object and returns the round trip light time from the spacecraft
        to the body.

        :param time: input time object
        :type time: Time
        :param time_reference: SCET, ERT or ETT
        :type time_reference: str
        :param spacecraft_id: spacecraft or target id
        :type spacecraft_id: int
        :param body_id: body or observer id
        :type body_id: int
        :return: round trip light time
        :rtype: Duration
        """
        downleg = Time.downleg(time, time_reference, spacecraft_id, body_id)
        down_time = time + downleg
        upleg = Time.upleg(down_time, time_reference, spacecraft_id, body_id)
        return downleg + upleg

    @staticmethod
    def downleg(time, time_reference='SCET', spacecraft_id=None, body_id=time_globals.EARTH_NAIF_ID):
        """
        Calculates the OWLT from the target_id to the observer_id.
        This calculation is different for SCET vs ERT/ETT.

        :param time: time to be used for OWLT calculation
        :type time: Time
        :param time_reference: SCET, ERT or ETT
        :type time_reference: str
        :param spacecraft_id: naif id of target spacecraft or body
        :type spacecraft_id: int
        :param body_id: naif id of observer spacecraft or body
        :type body_id: int
        :return: one way light time as a duration object
        :rtype: Duration
        """
        return Time.__downleg_et(time.to_et(), time_reference, Time.get_spacecraft_id(spacecraft_id), body_id)

    @staticmethod
    def upleg(time, time_reference = 'SCET', spacecraft_id=None, body_id=time_globals.EARTH_NAIF_ID):
        """
        Calculates and returns the OWLT from the observer_id to the
        target_id, the opposite of downleg. This calculation is different
        for SCET vs ERT/ETT.

        :param time: time to be used for OWLT calculation
        :type time: Time
        :param time_reference: SCET, ERT or ETT
        :type time_reference: str
        :param spacecraft_id: naif id of target spacecraft or body
        :type spacecraft_id: int
        :param body_id: naif id of observer spacecraft or body
        :type body_id: int
        :return: one way light time as a duration object
        :rtype: Duration
        """
        return Time.__upleg_et(time.to_et(), time_reference, Time.get_spacecraft_id(spacecraft_id), body_id)

    @staticmethod
    def from_ert(time_of_unknown_type, spacecraft_id=None, body_id=time_globals.EARTH_NAIF_ID):
        """
        Takes in a string or time object and returns a time object representing
        the SCET time.
        
        :param time_of_unknown_type: time string, time object, etc.
        :type time_of_unknown_type: object 
        :param spacecraft_id: spacecraft id for OWLT calculation
        :type spacecraft_id: int
        :return: time object
        :rtype: Time
        """
        t = Time(time_of_unknown_type)
        return t - Time.downleg(t, 'ERT', spacecraft_id, body_id)

    @staticmethod
    def from_ett(time_of_unknown_type, spacecraft_id=None, body_id=time_globals.EARTH_NAIF_ID):
        """
        Takes in a string or time object and returns a time object representing
        the SCET time.

        :param time_of_unknown_type: time string, time object, etc.
        :type time_of_unknown_type: object 
        :param spacecraft_id: spacecraft id for OWLT calculation
        :type spacecraft_id: int
        :return: time object
        :rtype: Time
        """
        t = Time(time_of_unknown_type)
        return t + Time.upleg(t, 'ETT', spacecraft_id, body_id)

    @staticmethod
    def from_fractional_sols(fractional_sols):
        """Takes a float that represents number of sols since the landing epoch
        and converts it to a time object.

        :param fractional_sols: fractional number of sols since landing epoch
        :type fractional_sols: float
        :return: time object corresponding to the time of day on the given sol
        :rtype: Time
        """
        sols = int(fractional_sols)
        decimal = fractional_sols - sols
        lmst_time_of_day = Duration(decimal * time_globals.SECONDS_PER_DAY)
        lmst_string = 'Sol-{:04d}M{}'.format(sols, lmst_time_of_day.to_string())

        return Time(lmst_string)

    @staticmethod
    def from_tai(tai):
        """
        Convert TAI seconds as a float to a time object.
        :param tai: TAI seconds
        :type tai: float
        :return: time object
        :rtype: Time
        """
        return Time(Time.tai2et(tai))

    @staticmethod
    def from_gps(gps):
        """
        Converts a GPST string into a time object.

        :param gps: time string for GPST
        :type gps: str
        :return: Time object
        :rtype: Time
        """
        dt_at_gps_epoch = Time(GPST_EPOCH).to_datetime()
        dt_at_input_time = Time(gps).to_datetime()
        tai_seconds_offset = (dt_at_input_time - dt_at_gps_epoch).total_seconds()
        return Time(GPST_EPOCH) + Duration(tai_seconds_offset)

    @staticmethod
    def from_gps_seconds(gps_seconds):
        """
        Converts GPS seconds as a float to a time object.

        :param gps_seconds: GPS seconds
        :type gps_seconds: float
        :return: time object
        :rtype: Time
        """
        tai_at_gps_epoch = Time(GPST_EPOCH).to_tai()  # this will be a large negative number of seconds
        return Time.from_tai(gps_seconds + tai_at_gps_epoch)

    @staticmethod
    def from_sclkd(sclkd, spacecraft_id=None):
        """
        Converts from a SCLKD float to a time object.

        :param sclkd: decimal SCLK value
        :param spacecraft_id: naif id of spacecraft
        :type spacecraft_id: int
        :return: time object corresponding to the SCLKD value
        :rtype: Time
        """
        # expecting the input to be a float, error if not
        if isinstance(sclkd, float) or isinstance(sclkd, int):
            regex_match = re.search(time_globals.SCLK_FLOAT_REGEX_EXACT, str(float(sclkd)))
            seconds = int(regex_match.group('seconds'))
            subseconds = float('0.' + regex_match.group('subsec'))
            corrected_subseconds = int(round(subseconds * Time.get_sclk_fractional_part(spacecraft_id)))
            sclk_string = '1/{}-{}'.format(seconds, corrected_subseconds)

            try:
                return Time(spice.scs2e(Time.get_spacecraft_id(spacecraft_id), sclk_string))

            except spice.stypes.SpiceyError as e:
                parse_spice_error(e)

        else:
            raise TimeFormatError('Error parsing SCLKD value {}. Value needed to be a float.'.format(sclkd))

    @staticmethod
    def from_sclk(sclk, spacecraft_id=None):
        """
        Converts an input SCLK string to a time object.

        :param sclk: SCLK string of format SSSSSSSSSS-FFFFF
        :type sclk: str
        :param spacecraft_id: naif id of spacecraft
        :type spacecraft_id: int
        :return: time object
        :rtype: Time
        """
        try:
            return Time(spice.scs2e(Time.get_spacecraft_id(spacecraft_id), sclk))

        except spice.stypes.SpiceyError as e:
            parse_spice_error(e)

    @staticmethod
    def from_lmst(lmst_string, lmst_sclk_id=None):
        """
        Converts an input LMST string into a time object.

        :param lmst_string: Mars time string of format Sol-####M##:##:##.###
        :type lmst_string: str
        :param lmst_sclk_id: SCLK ID of LMST file, usually spacecraft id followed by 900
        :type lmst_sclk_id: int
        :return: time object
        :rtype: Time
        """
        regex_match = re.match(time_globals.LMST_REGEX, lmst_string)
        if regex_match:
            # the decimal in SPICE is actually a number of "ticks" similar to SCLK
            if regex_match.group('decimal'):
                decimal = float('0.' + regex_match.group('decimal'))
            else:
                decimal = 0.0

            # convert the decimal to a fraction of the LMST modulus
            corrected_decimal = int(round(Time.LMST_FRACTIONAL_PART * decimal, 0))

            # note that the way spice takes decimals is :<decimal as number of ticks out of the modulus>
            spice_lmst_string = '{}:{}:{}:{}:{}'.format(
                regex_match.group('sol'),
                regex_match.group('hours'),
                regex_match.group('minutes'),
                regex_match.group('seconds'),
                str(corrected_decimal),
            )
            try:
                et = spice.scs2e(Time.get_lmst_sclk_id(lmst_sclk_id), spice_lmst_string)
                return Time(et)

            except spice.stypes.SpiceyError as e:
                parse_spice_error(e)

        else:
            raise TimeFormatError('Error parsing LMST string {}. String did not match'
                             ' expected regex'.format(lmst_string))
        
    @staticmethod
    def from_ltst(ltst, spacecraft_id=None, lmst_sclk_id=None):
        """
        Converts an input LTST string to a time object with ~1 second accuracy.
        This is orders of magnitude faster than the more accurate calculation.
        If a specific spacecraft id is given then the lmst sclk id is also needed,
        otherwise spacecraft id + 900 will be used (which is usually correct).

        The algorithm is:
        1. Assume the LTST time is LMST, then convert from LMST to SCET
        2. Convert from that SCET time to LTST
        3. Take the original LTST time and subtract and add 12 hours to it, then convert
           those two times as LMST to ET, and then again to LTST.
        4. Calculate the average mars second by taking the difference of the two LTST times
           and their associated ETs.
        5. Calculate the difference of the input LTST and calculated LTST
        6. Take the difference calculated by (5) and multiply it by the average mars
           second calculated by (4) to get the input LTST as ET.

        :param ltst: LTST string
        :type ltst: str
        :param spacecraft_id: spacecraft ID
        :type spacecraft_id: int
        :param lmst_sclk_id: sclk id for LMST conversion
        :type lmst_sclk_id: int
        :return: time object representing LTST time in SCET
        :rtype: Time
        """

        # get the lmst sclk id based on the inputs
        # spacecraft id + 900 is the standard, so if not provided then use that
        if lmst_sclk_id:
            updated_lmst_sclk_id = lmst_sclk_id

        elif Time.get_lmst_sclk_id(lmst_sclk_id):
            updated_lmst_sclk_id = Time.get_lmst_sclk_id(lmst_sclk_id)

        elif Time.get_spacecraft_id(spacecraft_id):
            updated_lmst_sclk_id = int(str(Time.get_spacecraft_id(spacecraft_id)) + '900')

        else:
            raise TimeConversionError('Error converting from LTST. Spacecraft ID has not been set.')

        # get the sol 0 LMST time since this algorithm relies on LMST
        lmst_epoch = Time.get_lmst_epoch(updated_lmst_sclk_id)

        # 1. Assume the LTST time is LMST, then convert from LMST to SCET
        lmst1 = Time.from_lmst(ltst.replace('T', 'M'), updated_lmst_sclk_id)

        # if the time is within 12 hours of LTST then give error because it is unreliable
        if lmst1 - lmst_epoch < Duration('12:00:00'):
            raise TimeConversionError('Error converting from LTST. Any LTST conversion within 12 hours '
                             'of the LMST epoch is unreliable.')

        # 2. Convert from that SCET time to LTST
        ltst2 = lmst1.to_ltst(spacecraft_id).replace('T', 'M')

        # 3. Take the original LTST time and subtract and add 12 hours to it, then convert
        #    those two times as LMST to ET, and then again to LTST.
        lmst_pre = lmst1 - Duration("M12:00:00")
        lmst_post = lmst1 + Duration("M12:00:00")

        ltst_pre = lmst_pre.to_ltst(spacecraft_id).replace('T', 'M')
        ltst_post = lmst_post.to_ltst(spacecraft_id).replace('T', 'M')

        # 4. Calculate the average mars second by taking the difference of the two LTST times
        #    and their associated ETs.
        lmst_diff = lmst_post - lmst_pre
        ltst_diff = Time.from_lmst(ltst_post, updated_lmst_sclk_id) - Time.from_lmst(ltst_pre, updated_lmst_sclk_id)
        avg_mars_sec = lmst_diff / ltst_diff

        # 5. Calculate the difference of the input LTST and calculated LTST
        input_ltst_diff = (Time(ltst2) - lmst1)

        # 6. Take the difference calculated by (5) and multiply it by the average mars
        #    second calculated by (4) to get the input LTST as ET.
        input_ltst_et = lmst1 - (input_ltst_diff * avg_mars_sec)

        return input_ltst_et

    @staticmethod
    def from_gst(gst_seconds, sol, last_local_midnight_time, last_local_midnight_sol, spacecraft_id=None):
        """
        Converts a GST (Generic Sol Time) number of seconds to a time object.
        :type gst_seconds: int
        :param gst_seconds: number of SCLK seconds since local midnight
        :type sol: int
        :param sol: sol number associated with this GST value
        :type last_local_midnight_time: Time
        :param last_local_midnight_time: value of the lcl_mdnt DP as a Time object
        :type last_local_midnight_sol: int
        :param last_local_midnight_sol: value of lcl_mdnt_sol DP
        :rtype: Time
        """
        return Time.from_sclkd(last_local_midnight_time.to_sclkd(spacecraft_id=spacecraft_id) + (sol - last_local_midnight_sol) * Time.GST_SECONDS_PER_SOL + gst_seconds, spacecraft_id=spacecraft_id)

    @staticmethod
    def from_timezone(time_of_unknown_type, timezone_name):
        """
        Converts a time from an input timezone to a UTC time object.

        :param time_of_unknown_type: time_of_unknown_type
        :type time_of_unknown_type: object
        :param timezone_name: name of timezone, must be compatible with pytz
        :type timezone_name: str
        :return: time object
        :rtype: Time
        """
        time_object = Time(time_of_unknown_type)
        offset = Time.__get_timezone_offset(time_object, timezone_name)
        return time_object - offset

    @staticmethod
    def from_pt(time_of_unknown_type):
        """
        Calls from_timezone on the PT time zone.

        :param time_of_unknown_type: time object, string, etc.
        :return: time object representing UTC time
        :rtype: Time
        """
        return Time.from_timezone(time_of_unknown_type, PACIFIC_TIME_ZONE)

    @staticmethod
    def from_pst(time_of_unknown_type):
        """
        Calls from_timezone on the PST time zone.

        :param time_of_unknown_type: time object, string, etc.
        :return: time object representing UTC time
        :rtype: Time
        """
        return Time.from_timezone(time_of_unknown_type, PST_TIME_ZONE)

    @staticmethod
    def from_pdt(time_of_unknown_type):
        """
        Calls from_timezone on the PDT time zone.

        :param time_of_unknown_type: time object, string, etc.
        :return: time object representing UTC time
        :rtype: Time
        """
        return Time.from_timezone(time_of_unknown_type, PDT_TIME_ZONE)

    @staticmethod
    def from_iso_week_day(year, week_num, day_num):
        """
        Takes in a year, week number and day number. The first week
        of the year is 1 and the first day of the week (Monday) is 1. Note that
        according to ISO the first week must contain January 4.

        :param year: year number
        :type year: int
        :param week_num: week number (first week is 1)
        :type week_num: int
        :param day_num: day number (Monday is 1)
        :type day_num: int
        :return: time object
        :rtype: Time
        """
        d = date(year, 1, 4) # get the start of the first week
        return Time(d + timedelta(weeks=week_num - 1, days=day_num - d.weekday() - 1))

    @staticmethod
    def load_kernel(kernel):
        """
        Loads an individual spice kernel.

        :param kernel: SPICE kernel to load
        :type kernel: str
        :return: None
        """
        if isinstance(kernel, str):
            try:
                spice.furnsh(kernel)

            except spice.stypes.SpiceyError as e:
                raise KernelError(e)

        else:
            raise KernelError('Error, expected input kernel {} to be a string.'.format(kernel))

    @staticmethod
    def load_kernels(kernel_list):
        """
        Loads a list of kernels.

        :param kernel_list: SPICE kernels to load
        :type kernel_list: list
        :return: None
        """
        if isinstance(kernel_list, list) or isinstance(kernel_list, set):
            for kernel in kernel_list:
                try:
                    spice.furnsh(kernel)

                except spice.stypes.SpiceyError as e:
                    raise KernelError(e)

        else:
            raise KernelError('Error, expected input kernel list {} to be a list.'.format(kernel_list))

    @staticmethod
    def reload_kernels(kernel_list):
        """
        Unloads all kernels which were loaded in time_config and loads the kernels
        in the input kernel list.
        
        :param kernel_list: new list of spice kernels to load
        :type kernel_list: list 
        :return: None
        """

        if isinstance(kernel_list, list) or isinstance(kernel_list, set):
            try:
                spice.kclear()

            except spice.stypes.SpiceyError as e:
                raise KernelError(e)

            for kernel in kernel_list:
                try:
                    spice.furnsh(kernel)

                except spice.stypes.SpiceyError as e:
                    raise KernelError(e)

        else:
            raise KernelError('Error, expected input kernel list {} to be a list.'.format(kernel_list))

    @staticmethod
    def unload_kernel(kernel, unload_basename=True, error_if_not_found=False):
        """
        Unloads a single kernel. Can either be the name of the file or
        the full path to the file.

        :param kernel: the filename of a single kernel
        :type kernel: str
        :param unload_basename: look by file basename for the kernel
        :type unload_basename: bool
        :param error_if_not_found: raise KernelMissingError if kernel is not found
        :type error_if_not_found: bool
        :rtype: None
        """
        # if the kernel is a string then unload it
        if isinstance(kernel, str):
            unloaded_kernel = False

            # unload the input full path to the kernel in the loaded list
            loaded_kernel_list = Time.get_all_loaded_kernels()
            if kernel in loaded_kernel_list:
                try:
                    spice.unload(kernel)
                    unloaded_kernel = True

                except spice.stypes.SpiceyError as e:
                    raise KernelError(e)

            # if specified, unload each kernel which has this basename
            elif unload_basename:
                for loaded_kernel in loaded_kernel_list:
                    if kernel == os.path.basename(loaded_kernel):
                        try:
                            spice.unload(loaded_kernel)
                            unloaded_kernel = True

                        except spice.stypes.SpiceyError as e:
                            raise KernelError(e)

            if error_if_not_found and not unloaded_kernel:
                raise KernelMissingError('Error unloading kernel {}. Kernel was not in '
                                 'list of loaded kernels {}.'.format(kernel, loaded_kernel_list))

        else:
            raise KernelError('Error, expected input kernel {} to be a string.'.format(kernel))

    @staticmethod
    def unload_kernels(kernel_list, unload_basename=True, error_if_not_found=False):
        """
        Unloads a list of kernels.

        :param kernel_list: a list of kernel names
        :type kernel_list: list
        :param unload_basename: look by file basename for the kernel
        :type unload_basename: bool
        :param error_if_not_found: raise KernelMissingError if kernel is not found
        :type error_if_not_found: bool
        :rtype: None
        """
        if isinstance(kernel_list, list) or isinstance(kernel_list, set):
            for kernel in kernel_list:
                Time.unload_kernel(kernel, unload_basename, error_if_not_found)

        else:
            raise KernelError('Error, expected input list of kernels {} to be a list.'.format(kernel_list))

    @staticmethod
    def unload_all_kernels(type='ALL'):
        """
        Unloads all spice kernels of the input type. Default is ALL.

        :param type: type of kernels to unload, default is ALL
        :type type: str
        """
        if type.upper() == 'ALL':
            try:
                spice.kclear()

            except spice.stypes.SpiceyError as e:
                raise KernelError(e)

        elif type.upper() in ['SPK', 'CK', 'PCK', 'EK', 'TEXT', 'META']:
            loaded_kernels = Time.get_all_loaded_kernels(type.upper())
            Time.unload_kernels(loaded_kernels)

        else:
            raise KernelError('Error, input kernel type {} was not in allowed list of types.'.format(type))

    @staticmethod
    def get_all_loaded_kernels(type='ALL'):
        """
        Returns a list of all currently loaded kernels.

        :return: list of loaded kernels
        :rtype: list
        """
        kernels_and_types = Time.get_all_loaded_kernels_with_types(type)

        return [k['kernel'] for k in kernels_and_types]

    @staticmethod
    def get_all_loaded_kernels_with_types(type='ALL'):
        """
        Returns a list of all currently loaded kernels.

        :return: list of dicts, where each dict has a loaded kernel and the type
        :rtype: list
        """
        kernels_and_types = []
        try:
            num_kernels = spice.ktotal(type)

        except spice.stypes.SpiceyError as e:
            raise KernelError(e)

        for i in range(0, num_kernels):
            try:
                kernel, kernel_type, _, _ = spice.kdata(i, type)
                kernels_and_types.append({'kernel': kernel, 'type': kernel_type})

            except spice.stypes.SpiceyError as e:
                raise KernelError(e)

        return kernels_and_types

    @staticmethod
    def get_spacecraft_id(override_spacecraft_id=None):
        """
        Returns the spacecraft ID, but allows users to pass a value to override
        the value it would otherwise return. This is needed specifically for the
        methods which want to get the new default spacecraft ID.

        :param override_spacecraft_id: non-default spacecraft ID to use
        :type override_spacecraft_id: int
        :return: spacecraft id
        :rtype: int
        """
        if isinstance(override_spacecraft_id, int):
            return override_spacecraft_id

        return Time.SPACECRAFT_ID

    @staticmethod
    def get_lmst_sclk_id(override_lmst_sclk_id=None):
        """
        Returns the LMST SCLK ID, but allows users to pass a value to override
        the value it would otherwise return. This is needed specifically for the
        methods which want to get the new default LMST SCLK ID.

        :param override_lmst_sclk_id: non-default lmst sclk ID to use
        :type override_lmst_sclk_id: int
        :return: lmst sclk id
        :rtype: int
        """
        if isinstance(override_lmst_sclk_id, int):
            return override_lmst_sclk_id

        return Time.LMST_SCLK_ID

    @staticmethod
    def get_time_output_precision(override_time_decimal_precision=None):
        """
        Returns the time decimal precision, but allows users to pass a value to override
        the value it would otherwise return. This is needed specifically for the
        methods which want to get the new default time decimal precision.

        :param override_time_decimal_precision: non-default precision to use
        :type override_time_decimal_precision: int
        :return: time decimal precision
        :rtype: int
        """
        if isinstance(override_time_decimal_precision, int):
            return override_time_decimal_precision

        return Time.OUTPUT_DECIMAL_PRECISION

    @staticmethod
    def get_sclk_fractional_part(spacecraft_id=None):
        """
        Returns the SCLK fractional part from the SCLK kernel.

        :param spacecraft_id: NAIF spacecraft id
        :type spacecraft_id: int
        :return: None
        """
        updated_spacecraft_id = Time.get_spacecraft_id(spacecraft_id)

        if updated_spacecraft_id in SCLK_FRACTIONAL_PART_TO_SCID_DICT:
            return SCLK_FRACTIONAL_PART_TO_SCID_DICT[updated_spacecraft_id]

        else:
            try:
                # moduli[0] is the max number of seconds the clock can count, and moduli[1] is
                # the number of sub-second tics
                quantity_needed = 'SCLK01_MODULI_' + str(abs(updated_spacecraft_id))
                moduli = spice.gdpool(quantity_needed, 0, 2)
                sclk_fractional_part = moduli[1]
                SCLK_FRACTIONAL_PART_TO_SCID_DICT[updated_spacecraft_id] = sclk_fractional_part
                return sclk_fractional_part

            except spice.stypes.SpiceyError as e:
                raise TimeConversionError(e)

    @staticmethod
    def get_lmst_epoch(lmst_sclk_id=None):
        """
        Returns a time object representing Sol-0000M00:00:00.
        :param lmst_sclk_id:
        :return:
        """
        updated_lmst_sclk_id = Time.get_lmst_sclk_id(lmst_sclk_id)
        if updated_lmst_sclk_id not in LMST_EPOCH_TO_SCID_DICT:
            LMST_EPOCH_TO_SCID_DICT[updated_lmst_sclk_id] = Time.from_lmst('Sol-0000M00:00:00', updated_lmst_sclk_id)

        return LMST_EPOCH_TO_SCID_DICT[updated_lmst_sclk_id]

    @staticmethod
    def et2tai(et):
        """
        Takes in ET seconds and returns TAI seconds, which is needed for
        comparing with durations.

        :param et: ET seconds
        :type et: float
        :return: TAI seconds
        :rtype: float
        """
        try:
            return spice.unitim(et, 'ET', 'TAI')

        except spice.stypes.SpiceyError as e:
            parse_spice_error(e)

    @staticmethod
    def tai2et(tai):
        """
        Takes in TAI seconds and returns ET seconds.

        :param tai: TAI seconds
        :type tai: float
        :return: ET seconds
        :rtype: float
        """
        try:
            return spice.unitim(tai, 'TAI', 'ET')

        except spice.stypes.SpiceyError as e:
            parse_spice_error(e)

    @staticmethod
    def now():
        """
        Returns the current time as a time object.

        :return: current time
        :rtype: Time
        """
        return Time(datetime.utcnow())

    @staticmethod
    def strptime(time_string, time_format_string):
        """
        Takes in a time string and a format string, which uses the syntax from
        Python datetime.strptime. Returns a time object.

        :param time_string:
        :param time_format_string:
        :return:
        """
        return Time(datetime.strptime(time_string, time_format_string))

    @staticmethod
    def __calculate_et(time_of_unknown_type):
        """
        Calculates ET based on the input time, depending on its type and format.

        :param time_of_unknown_type: input time string, datetime, or ephemeris time
        :return: ephemeris time seconds since J2000
        :rtype: float
        """

        # if a string is given then convert to ET depending on the REGEX
        if isinstance(time_of_unknown_type, str):
            scrubbed_string = time_of_unknown_type.strip()

            if scrubbed_string == '':
                return 0
            elif re.match(time_globals.LMST_REGEX, scrubbed_string):
                return Time.from_lmst(scrubbed_string).to_et()
            else:
                try:
                    return spice.utc2et(scrubbed_string)

                except spice.stypes.SpiceyError as e:
                    parse_spice_error(e)

        # if a datetime is given, convert to ET
        elif isinstance(time_of_unknown_type, datetime) or isinstance(time_of_unknown_type, date):
            try:
                return spice.utc2et(str(time_of_unknown_type))

            except spice.stypes.SpiceyError as e:
                parse_spice_error(e)

        # if an int or float is given, assume it represents seconds since the J2000 epoch
        elif isinstance(time_of_unknown_type, float) or isinstance(time_of_unknown_type, int):
            return float(time_of_unknown_type)

        # if it is a time object then it is easy
        elif isinstance(time_of_unknown_type, Time):
            return time_of_unknown_type.to_et()

        elif time_of_unknown_type == None:
            return 0

        # if it is none of these then try casting to a string, otherwise give error
        # this is needed for unicode in python 2
        else:
            try:
                return Time.__calculate_et(str(time_of_unknown_type))
            except:
                raise TimeFormatError(
                    "Value passed to Time constructor must be datetime, UTC string, LMST string, "
                    "int or float number of seconds, int sol number or float fractional sol number, "
                    "but was:\n{}".format(time_of_unknown_type))

    @staticmethod
    def __calculate_mars_longitude(et, spacecraft_id=None):
        """
        Calculates the longitude in radians of the input spacecraft at the given time.

        :param et: ephemeris time seconds since J2000
        :type et: float
        :param spacecraft_id: naif id of spacecraft
        :type spacecraft_id: int
        :return: longitude of spacecraft on mars in radians
        :rtype: float
        """
        frame = 'IAU_MARS'
        aberration_correction = 'NONE'
        try:
            position_vector, _ = spice.spkezp(
                Time.get_spacecraft_id(spacecraft_id),
                et,
                frame,
                aberration_correction,
                time_globals.MARS_NAIF_ID)

            _, longitude_rad, _ = spice.reclat(position_vector)
            return longitude_rad

        except spice.stypes.SpiceyError as e:
            parse_spice_error(e)

    @staticmethod
    def __reformat_spice_lmst(spice_lmst_string, precision=None):
        """
        Reformats the SPICE LMST output into the standard LMST string format.

        :param spice_lmst_string: SPICE LMST output
        :type spice_lmst_string: str
        :param precision: number of digits for output LMST string decimals
        :type precision: int
        :return: standard LMST format
        :rtype: str
        """
        # first we need to parse the SPICE LMST string
        regex_match = re.match(time_globals.SPICE_LMST_REGEX_EXACT, spice_lmst_string)
        if regex_match:
            # we need to convert to a duration so we can round the decimals easily
            sol_number = int(regex_match.group('sol'))
            mars_dur = Duration('{}:{}:{}.{}'.format(
                regex_match.group('hour'),
                regex_match.group('min'),
                regex_match.group('sec'),
                regex_match.group('subsec')))

            # including the precision here is how we round the mars duration
            mars_dur_regex_match = re.search(time_globals.DURATION_EXACT_REGEX,
                                             mars_dur.to_string(Time.get_time_output_precision(precision)))

            # if the duration is greater than 1 day then we need to add the day to the sol number
            if mars_dur_regex_match.group('days'):
                sol_number += int(mars_dur_regex_match.group('days'))

            # return the formatted string
            return 'Sol-{:04d}M{}'.format(sol_number, mars_dur_regex_match.group('time_of_day'))

        else:
            raise TimeFormatError('Error parsing SPICE LMST string {}. String did not match'
                             ' expected regex'.format(spice_lmst_string))

    @staticmethod
    def __reformat_spice_ltst(lmst_string, ltst_hr, ltst_min, ltst_sec):
        """
        Changes the SPICE LST output (hrs, mins, secs) into an LTST string which
        includes a sol number. Calculates sol number using LMST string.

        :param lmst_string: LMST string corresponding to the same utc time as the LTST conversion
        :type lmst_string: str
        :param ltst_hr: hours from spice LST calculation
        :type ltst_hr: int
        :param ltst_min: minutes from spice LST calculation
        :type ltst_min: int
        :param ltst_sec: seconds from spice LST calculation
        :type ltst_sec: int
        :return: LTST string with sol number and time of day
        :rtype: str
        """
        # the LST string doesn't have a sol number associated with it, so calculate it using LMST
        # assume that LMST is within 12 hours of LTST
        offset = Duration('12:00:00')
        lmst_time_of_day = Duration(time_globals.LMST_REGEX.match(
            lmst_string).group('time_of_day'))
        ltst_time_of_day = Duration('{}:{}:{}'.format(ltst_hr, ltst_min, ltst_sec))

        lmst_sols = int(time_globals.LMST_REGEX.match(lmst_string).group('sol'))

        # LMST TOD = 23:00:00, LTST = 02:00:00 -> LTST sols = LMST sols + 1
        if lmst_time_of_day > ltst_time_of_day + offset:
            ltst_sols = lmst_sols + 1

        # LMST TOD = 05:00:00, LTST = 21:00:00 -> LTST sols = LMST sols - 1
        elif lmst_time_of_day + offset < ltst_time_of_day:
            ltst_sols = lmst_sols - 1

        else:
            ltst_sols = lmst_sols

        return 'Sol-{:04d}T{:02d}:{:02d}:{:02d}'.format(
            ltst_sols, int(ltst_hr), int(ltst_min), int(ltst_sec))

    @staticmethod
    def __time_of_day_to_fractional_day(time_of_day):
        """
        Converts an input time of day duration to a fractional day.

        :param time_of_day: duration object corresponding to a time of day
        :type time_of_day: Duration
        :return: fractional day
        :rtype: float
        """
        return time_of_day.to_seconds() / time_globals.SECONDS_PER_DAY

    @staticmethod
    def __get_timezone_offset(time, timezome_name):
        """
        Calculates the offset required to go from utc to the input timezone at
        the input time.

        :param time: time object to be used for the calculation
        :type time: Time
        :param timezome_name: name of timezone, which is valid in pytz
        :type timezome_name: str
        :return: offset from utc to timezone
        :rtype: Duration
        """
        tz = pytz.timezone(timezome_name)
        dt = Time.__utc_to_datetime(time.to_utc())
        t_utc = Time(dt.strftime("%Y-%jT%H:%M:%S.%f"))
        t_tz = Time(tz.fromutc(dt).strftime("%Y-%jT%H:%M:%S.%f"))

        return t_tz - t_utc

    @staticmethod
    def __downleg_et(et, time_reference='SCET', spacecraft_id=None, body_id=time_globals.EARTH_NAIF_ID):
        """
        Calculates OWLT and defaults to target_id = SPACECRAFT_ID and
        observer_id = time_globals.EARTH_NAIF_ID. Calculates the OWLT
        from the target_id to the observer_id, but is different depending
        on whether the ET represents SCET, ERT or ETT.

        :param et: ephemeris time seconds since J2000
        :type et: float
        :param time_reference: SCET, ERT or ETT
        :type time_reference: str
        :param spacecraft_id: naif id of target spacecraft or body
        :type spacecraft_id: int
        :param body_id: naif id of observer spacecraft or body
        :type body_id: int
        :return: one way light time as a duration object
        :rtype: Duration
        """
        # this method gets the default spacecraft id if none is passed
        # this is needed to allow users to update the default
        updated_spacecraft_id = Time.get_spacecraft_id(spacecraft_id)

        # the calculation is different for spacecraft vs ground time
        if time_reference == 'SCET':
            return Time.owlt(et, updated_spacecraft_id, '->', body_id)

        elif time_reference == 'ERT' or time_reference == 'ETT':
            return Time.owlt(et, body_id, '<-', updated_spacecraft_id)

        else:
            raise TimeConversionError('Error calculating downleg with input time_reference {}. This value must be either'
                             'SCET, ERT, or ETT.'.format(time_reference))

    @staticmethod
    def __upleg_et(et, time_reference='SCET', spacecraft_id=None, body_id=time_globals.EARTH_NAIF_ID):
        """
        Calculates and returns the OWLT from the observer_id to the
        target_id, the opposite of downleg.

        :param et: ephemeris time seconds since J2000
        :type et: float
        :param time_reference: SCET, ERT or ETT
        :type time_reference: str
        :param spacecraft_id: naif id of target spacecraft or body
        :type spacecraft_id: int
        :param body_id: naif id of observer spacecraft or body
        :type body_id: int
        :return: one way light time as a duration object
        :rtype: Duration
        """
        # this method gets the default spacecraft id if none is passed
        # this is needed to allow users to update the default
        updated_spacecraft_id = Time.get_spacecraft_id(spacecraft_id)

        # the calculation is different for spacecraft vs ground time
        if time_reference == 'SCET':
            return Time.owlt(et, updated_spacecraft_id, '<-', body_id)

        elif time_reference == 'ERT' or time_reference == 'ETT':
            return Time.owlt(et, body_id, '->', updated_spacecraft_id)

        else:
            raise TimeConversionError('Error calculating upleg with input time_reference {}. This value must be either'
                             'SCET, ERT, or ETT.'.format(time_reference))

    @staticmethod
    def __utc_to_datetime(utc):
        """
        Converts a UTC string to a datetime object.

        :param utc: UTC string
        :type utc: str
        :return: datetime object corresponding to UTC time
        :rtype: datetime
        """
        try:
            return datetime.strptime(utc, time_globals.UTC_FMT_FULL)
        except ValueError:
            return datetime.strptime(utc, time_globals.UTC_FMT_TRUNCATED)

    @staticmethod
    def __get_year_time(input_time):
        """
        Returns the start of the current year as a time object.

        :param input_time: time object
        :type input_time: Time
        :return: time object representing start of year
        :rtype: Time
        """
        regex_match = re.search(time_globals.UTC_EXACT_REGEX, input_time.to_utc())
        return Time('{}-001T00:00:00'.format(regex_match.group('year')))


class EpochRelativeTime(Time):
    """
    This class represents epoch-relative times and inherits from the Time class in the same package in order to
    inter-operate with it as smoothly as possible. In addition to et and tai from the absolute base class,
    this gets two new fields: a string epoch name and a Duration offset from that epoch. The to_string() method is overwritten
    to preserve those quantities in file outputs, but all other output methods are not, since one needs an absolute times
    to do comparisons or geometric calculations.
    """
    __epochs__ = {}

    @classmethod
    def add_epoch(cls, epoch_name, epoch_time):
        """
        Adds an epoch to the epoch dict, which can be used when creating EpochRelativeTime objects.
        :type epoch_name: str
        :param epoch_name: name of the epoch
        :type epoch_time: Time
        :param epoch_time: Time object associated with this epoch name
        """
        cls.__epochs__[epoch_name] = epoch_time

    @classmethod
    def set_epochs(cls, new_epochs):
        """
        Sets the epoch dict to be the input dict. The dict should have epoch names as keys
        and Time objects as values.
        :type new_epochs: dict
        :param new_epochs: dict of epochs
        """
        cls.__epochs__ = new_epochs

    @classmethod
    def remove_epoch(cls, epoch_name):
        """
        Removes an epoch from the dict of epochs.
        :type epoch_name: str
        :param epoch_name: epoch name to remove
        """
        cls.__epochs__.pop(epoch_name, None)

    @classmethod
    def is_epoch_defined(cls, epoch_name):
        """
        Returns whether or not the epoch name is available in the dict of epochs.
        :type epoch_name: str
        :param epoch_name: epoch name to check
        :rtype: bool
        """
        return epoch_name in cls.__epochs__

    @classmethod
    def get_epochs(cls):
        """
        Returns the dict of epochs of epoch name to Time object.
        :rtype: dict
        """
        return cls.__epochs__

    def __init__(self, *args):
        if len(args) < 2:
            self.epoch_name, self.offset = EpochRelativeTime.__parse_epoch_relative_string(args[0])
        else:
            self.epoch_name = args[0]
            self.offset = args[1]
        # the below line sets self.et and self.tai
        super().__init__(time_of_unknown_type=EpochRelativeTime.__epochs__[self.epoch_name] + self.offset)

    def __repr__(self):
        return self.to_string()

    def __add__(self, duration):
        return EpochRelativeTime(self.epoch_name, self.offset + duration)

    def __sub__(self, duration_or_time):
        if isinstance(duration_or_time, Duration):
            return EpochRelativeTime(self.epoch_name, self.offset - duration_or_time)
        else:
            return super().__sub__(duration_or_time)

    def to_string(self, precision=None, format_type=''):
        """
        Returns a string representing the epoch relative time
        :type precision: int
        :param precision: precision for duration portion of epoch relative time string output
        :type format_type: str
        :param format_type: Not used for EpochRelativeTime string but needed for Time to_string method
        :rtype: str
        """
        sign = '+' if self.offset >= Duration(0) else '-'
        return self.epoch_name + sign + self.offset.abs().to_string(Duration.get_duration_decimal_precision(precision))

    @classmethod
    def __parse_epoch_relative_string(cls, time_string):
        """
        Parses an input string into an epoch name and offset Duration. Not meant for use outside of this class.
        :type time_string: str
        :rtype: tuple
        """
        regex_match = re.match(time_globals.EPOCH_RELATIVE_REGEX, time_string.strip())
        if regex_match:
            epoch_name = regex_match.group('epoch_name')
            sign = regex_match.group('relative_sign')
            offset = Duration(regex_match.group('offset'))

            if epoch_name not in cls.__epochs__:
                raise EpochRelativeTimeError('Could not create epoch-relative time ' + time_string + ' since epoch ' + epoch_name
                                 + ' was not found in list of defined epochs: ' + ','.join(cls.__epochs__.keys()))

            coefficient = -1 if (sign == '-') else 1
            return epoch_name, offset * coefficient

        else:
            raise EpochRelativeTimeFormatError('Error parsing epoch-relative time string {}. String did not match'
                             ' expected regex'.format(time_string))


def __build_parser_and_parse():
    """
    Defines the command line arguments using argparse.
    This function is only meant to be used by the CLI.
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version',
                        action='version',
                        version="%s %s" % ('%(prog)s', __version__),
                        help='print version number and exit')

    parser.add_argument('-k', '--kernels',
                        action='store_true',
                        help='print loaded kernels and exit')

    mutually_exclusive_arguments = parser.add_argument_group('Mutually Exclusive Required Arguments')
    mutually_exclusive_arguments.add_argument('-t', '--time',
                                              help='Input time to be converted',
                                              required=False)

    mutually_exclusive_arguments.add_argument('-n', '--now',
                                              action='store_true',
                                              help='Print the current time',
                                              required=False)

    optional_arguments = parser.add_argument_group('Optional Arguments')
    optional_arguments.add_argument('-i', '--inputType',
                                    choices=ALLOWED_INPUT_TYPES,
                                    help='Time type of input time. Will try to figure out automatically'
                                         'if not provided.',
                                    required=False)

    optional_arguments.add_argument('-o', '--outputType',
                                    choices=ALLOWED_OUTPUT_TYPES,
                                    help='Time type for output time. Will print all output types if not '
                                         'provided.',
                                    required=False)

    optional_arguments.add_argument('-a', '--add',
                                    help='Add an earth or mars duration. (Mars duration syntax has M instead '
                                         'of T)',
                                    required=False)

    optional_arguments.add_argument('-s', '--subtract',
                                    help='Subtract an earth or mars duration. (Mars duration syntax has M instead '
                                         'of T)',
                                    required=False)

    optional_arguments.add_argument('-c', '--config',
                                    help='Chronos config file containing paths to kernels and the spacecraft id. '
                                         'If not provided then the script will look at CHRONOS environment '
                                         'variables.',
                                    required=False)

    optional_arguments.add_argument('-f', '--fetch',
                                    help='Download the latest kernels for the input mission. Only missions which '
                                         'support the chronos setup configuration on the NAIF server are currently '
                                         'supported. Kernels will be downloaded into a directory structure in the '
                                         'current directory. This directory can be moved elsewhere if the '
                                         'CHRONOS_SETUP environment variable path is updated to reflect the new location.',
                                    required=False)

    optional_arguments.add_argument('-l', '--latest',
                                    help='Check if the latest kernels are being used. Only missions which '
                                         'support the chronos setup configuration on the NAIF server are currently '
                                         'supported.',
                                    action='store_true',
                                    required=False)

    optional_arguments.add_argument('-d', '--debug',
                                    help='Show full traceback on errors.',
                                    action='store_true',
                                    required=False)

    return parser.parse_args()


def __validate_args(args):
    """
    Checks that the input arguments are valid and throws an error
    if not.
    This function is only meant to be used by the CLI.
    :param args: argparse object
    :return:
    """
    # check that input file exists if given
    if args.config:
        if not os.path.isfile(args.config):
            raise JplTimeError('Error: input chronos config file {} does not exist or is not '
                             'a file.'.format(args.config))

    # enforce mutual exclusivity
    if args.time and args.now:
        raise JplTimeError('Error, -n and -t are mutually exclusive')

    if not args.time and not args.now and not args.kernels and not args.fetch and not args.latest:
        raise JplTimeError('Error, at least one of -t or -n must be provided')

    if args.fetch and args.latest:
        raise JplTimeError('Error, only one of -f and -l can be provided')


def load_chronos_config(chronos_config_path=None):
    """
    Optionally takes in the path to a chronos config file and parses it to find
    all kernels to load. If a path is not provided then this function will look
    for the file using CHRONOS_SETUP environment variables.

    :param chronos_config_path: path to chronos config file
    :type chronos_config_path: str
    :return: None
    """
    try:
        spacecraft_id, lmst_sclk_id, kernels = \
            chronos_input_parsing.__get_spice_inputs_from_chronos_files(chronos_config_path)

    except ValueError as e:
        raise KernelError(e)

    Time.set_spacecraft_id(spacecraft_id)
    Time.set_lmst_sclk_id(lmst_sclk_id)
    Time.load_kernels(list(kernels))


def download_latest_kernels(spacecraft_id=None, progress_bar=False):
    """
    Downloads the latest kernels used for the input spacecraft id or currently set spacecraft id
    based on the latest chronos setup file on NAIF. Only supports missions which currently support
    the NAIF chronos setup infrastructure. Returns a list of any missing kernels. If progress bar is
    set to True then a progress bar will be written to the terminal.
    :type spacecraft_id: int
    :type progress_bar: bool
    :rtype: str
    """
    if not Time.get_spacecraft_id() and not spacecraft_id:
        raise KernelError('Error, could not download for latest kernels because spacecraft id has not been provided'
                         'and is not set in Time class.')

    updated_spacecraft_id = spacecraft_id if spacecraft_id else Time.get_spacecraft_id()

    try:
        return fetch_latest_kernels.__download_chronos_setup_and_kernels(updated_spacecraft_id, progress_bar)
    except Exception as e:
        raise KernelError(e)


def check_for_latest_kernels(spacecraft_id=None):
    """
    Checks if the kernels being used for the input spacecraft id or currently set spacecraft id
    are the latest by comparing to NAIF. Only supports missions which currently support the NAIF
    chronos setup infrastructure. Returns a list of any missing kernels.
    :type spacecraft_id: int
    :rtype: list
    :return: list of missing kernels
    """
    if not Time.get_spacecraft_id() and not spacecraft_id:
        raise KernelError('Error, could not check for latest kernels because spacecraft id has not been provided'
                         'and is not set in Time class.')

    updated_spacecraft_id = spacecraft_id if spacecraft_id else Time.get_spacecraft_id()

    try:
        missing_kernels = fetch_latest_kernels.__check_if_loaded_kernels_are_latest(
            Time.get_all_loaded_kernels(), updated_spacecraft_id)

        return missing_kernels

    except Exception as e:
        raise KernelError(e)


def create_jpl_time_object(input_time, input_type):
    """
    Creates a time object from the input string based on the specified
    input type.
    This function is meant to primarily be used by the CLI and not for normal usage.
    However, this can be used to create a Time object if one is unable to use static methods.

    :param input_time: string representation of time
    :type input_time: str
    :param input_type: 'scet', 'utc', 'ert', 'ett', 'gps', 'pt', 'isoc', 'et', 'sclk', 'sclkd', 'lmst', 'ltst'
    :type input_type: str
    :return:
    """
    if input_type in ['scet', 'utc', 'isoc', 'lmst']:
        return Time(input_time)

    elif input_type == 'ert':
        return Time.from_ert(input_time)

    elif input_type == 'ett':
        return Time.from_ett(input_time)

    elif input_type == 'gps':
        return Time.from_gps(input_time)

    elif input_type == 'pt':
        return Time.from_pt(input_time)

    elif input_type == 'pst':
        return Time.from_pst(input_time)

    elif input_type == 'pdt':
        return Time.from_pdt(input_time)

    if input_type == 'et':
        return Time(float(input_time))

    elif input_type == 'sclk':
        return Time.from_sclk(input_time)

    elif input_type == 'sclkd':
        return Time.from_sclkd(float(input_time))

    elif input_type == 'ltst':
        return Time.from_ltst(input_time)

    else:
        raise JplTimeError('Error in convert_jpl_time: input time type {} was not an allowed type.'.format(input_type))


def output_jpl_time_in_format(time_object, output_type):
    """
    Takes in a Time object and returns a string depending on the
    string output type.
    This function is meant to primarily be used by the CLI and not for normal usage.

    :param time_object: Time object
    :type time_object: Time
    :param output_type: string name of output type (see ALLOWED_OUTPUT_TYPES)
    :type output_type: str
    :return: string representing time
    :rtype: str
    """
    if output_type == 'scet':
        return time_object.to_scet()

    if output_type == 'utc':
        return time_object.to_utc()

    elif output_type == 'ert':
        return time_object.to_ert()

    elif output_type == 'ett':
        return time_object.to_ett()

    elif output_type == 'gps':
        return time_object.to_gps()

    elif output_type == 'pt':
        # reformat pt to month/day/year hh:mm:ss
        dt = Time(time_object.to_pt()).to_datetime()
        return dt.strftime('%m/%d/%Y %H:%M:%S.%f')[0:-3]

    elif output_type == 'pst':
        # reformat pt to month/day/year hh:mm:ss
        dt = Time(time_object.to_pst()).to_datetime()
        return dt.strftime('%m/%d/%Y %H:%M:%S.%f')[0:-3]

    elif output_type == 'pdt':
        # reformat pt to month/day/year hh:mm:ss
        dt = Time(time_object.to_pdt()).to_datetime()
        return dt.strftime('%m/%d/%Y %H:%M:%S.%f')[0:-3]

    elif output_type == 'isoc':
        return time_object.to_isoc()

    elif output_type == 'et':
        return repr(time_object.to_et())

    elif output_type == 'sclk':
        return time_object.to_sclk()

    elif output_type == 'sclkd':
        return repr(time_object.to_sclkd())

    elif output_type == 'lmst':
        return time_object.to_lmst()

    elif output_type == 'ltst':
        return time_object.to_ltst()

    elif output_type == 'downleg':
        return Time.downleg(time_object).to_string()

    elif output_type == 'upleg':
        return Time.upleg(time_object).to_string()

    elif output_type == 'rtlt':
        return Time.rtlt(time_object).to_string()

    else:
        raise JplTimeError('Error in output_jpl_time_in_format: output time type '
                         '{} was not an allowed type.'.format(output_type))


def convert_jpl_time(input_time, input_type, output_type):
    """
    Converts an input time string from one time type to another based on the
    input_type and output_type.
    This function is meant to primarily be used by the CLI and not for normal usage.

    :param input_time: input time string
    :type input_time: str
    :param input_type: see ALLOWED_INPUT_TYPES
    :type input_type: str
    :param output_type: see ALLOWED_OUTPUT_TYPES
    :type output_type: str
    :return: the specified output type, usually a string or float
    """
    time_object = create_jpl_time_object(input_time, input_type)
    output_string = output_jpl_time_in_format(time_object, output_type)

    return output_string


def convert_to_all_formats(input_time):
    """
    Converts an input time to all formats and returns them in a dict.
    This function is meant to primarily be used by the CLI and not for normal usage.
    :param input_time: input time object
    :type input_time: Time
    :return: dict of all allowed time types as strings
    :rtype: dict
    """
    time_dict = {}
    for output_type in ALLOWED_OUTPUT_TYPES:
        try:
            time_dict[output_type] = output_jpl_time_in_format(input_time, output_type)

        # I know I shouldn't be using a bare except here, but it's just for
        # printing out to the terminal
        except:
            time_dict[output_type] = 'N/A'

    return time_dict


def __print_time_dict(time_dict, input_type):
    """
    Takes in a time dict which has each of the ALLOWED_OUTPUT_TYPES.
    This function is meant to only be used by CLI.
    :param time_dict:
    :param input_type:
    :return:
    """
    for time_type in ALLOWED_OUTPUT_TYPES:
        print('{}{:10}{}'.format(
            '* ' if input_type == time_type else '  ',
            time_type,
            time_dict[time_type]
        ))


# attempt to import chronos config, do nothing if not found
try:
    load_chronos_config()
    SPICE_IMPORTED = True

except ValueError:
    SPICE_IMPORTED = False


def main():
    """
    Allows users to convert times using the time class from the command line.
    :return:
    """
    # get the input parameters and make sure they are valid
    args = __build_parser_and_parse()
    __validate_args(args)

    if not args.debug:
        sys.tracebacklimit = 0

    if args.fetch:
        chronos_setup_name = download_latest_kernels(args.fetch, True)
        print(
            'Run the following command or add to your .cshrc/.bash_profile to automatically find the kernels:\n'
            'shell: setenv CHRONOS_SETUP "{}"\nbash:  export CHRONOS_SETUP="{}"'.format(chronos_setup_name, chronos_setup_name))
        exit()

    if args.latest:
        missing_kernels = check_for_latest_kernels()
        updated_mission = fetch_latest_kernels.SUPPORTED_MISSIONS[str(Time.get_spacecraft_id())]
        if missing_kernels:
            print('Latest kernels on NAIF server for {} are not being used:'.format(updated_mission.lower()))
            print('    Missing kernels: {}'.format(', '.join(missing_kernels)))

        else:
            print('Kernels are up to date with latest on NAIF server.')
        exit()

    # get the spice inputs and update spice
    if args.config:
        load_chronos_config(args.config)
    elif not SPICE_IMPORTED:
        load_chronos_config()

    # if -k was given, print kernels and exit
    if args.kernels:
        print('Loaded Kernels:')
        for kernel in Time.get_all_loaded_kernels():
            print('    ' + kernel)
        exit()

    # get the input time and type
    if args.time:
        input_time_string = args.time
    else:
        input_time_string = Time.now().to_utc()

    # get the input type
    if args.inputType:
        input_type = args.inputType
    else:
        if re.search(time_globals.LMST_EXACT_REGEX, input_time_string):
            input_type = 'lmst'
        else:
            input_type = 'scet'

    # get the time object based on the inputType
    input_time = create_jpl_time_object(input_time_string, input_type)

    # add and subtract if specified
    if args.add:
        input_time += Duration(args.add)

    if args.subtract:
        input_time -= Duration(args.subtract)

    # output the strings
    if args.outputType:
        print(output_jpl_time_in_format(input_time, args.outputType))
    else:
        time_dict = convert_to_all_formats(input_time)
        __print_time_dict(time_dict, input_type)


if __name__ == '__main__':
    main()
