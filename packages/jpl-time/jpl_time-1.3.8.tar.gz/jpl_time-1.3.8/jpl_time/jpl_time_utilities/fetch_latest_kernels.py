"""
This script contains functions for getting the latest kernels from the
NAIF website https://naif.jpl.nasa.gov/pub/naif/
"""

import re
import os
import tempfile
import filecmp
import sys
from datetime import datetime, timedelta

if sys.version_info.major == 3:
    from urllib.request import urlopen
    from urllib.error import HTTPError
else:
    from urllib2 import urlopen
    from urllib2 import HTTPError

try:
    from chronos_input_parsing import __get_kernels_from_chronos_setup_contents
    from utility_functions import progress_bar
except ImportError:
    from jpl_time.jpl_time_utilities.chronos_input_parsing import __get_kernels_from_chronos_setup_contents
    from jpl_time.jpl_time_utilities.utility_functions import progress_bar

__program__ = 'fetch_latest_kernels.py'
__author__  = 'Forrest Ridenhour'
__project__ = 'Mars2020'
__version__ = '1.0'
__dependencies__ = 'jpl_time.py'


SUPPORTED_MISSIONS = {
    '189':      'INSIGHT',
    '-189':     'INSIGHT',
    'NSY':      'INSIGHT',
    'NSYT':     'INSIGHT',
    'INSIGHT':  'INSIGHT',
    '76':       'MSL',
    '-76':      'MSL',
    'MSL':      'MSL',
    '168':      'MARS2020',
    '-168':     'MARS2020',
    'M20':      'MARS2020',
    'M2020':    'MARS2020',
    'MARS2020': 'MARS2020'
}

NAIF_URL = 'https://naif.jpl.nasa.gov/pub/naif/'
CHRONOS_DIRECTORY = 'https://naif.jpl.nasa.gov/pub/naif/{}/misc/chronos/setups/'
KERNEL_BASE_DIRECTORY = 'https://naif.jpl.nasa.gov/pub/naif/{}/kernels'

NAIF_TABLE_REGEX = re.compile('<pre>([a-zA-Z0-9_\-<>\s,;:="\n<>\.\?\/\[\]\|\(\)#&@]*)</pre>')
NAIF_DATA_REGEX = re.compile('<a href=".*">([a-zA-Z_\-0-9\.]+)</a>\s*(\d{2}-\w{3}-\d{4}\s\d{2}:\d{2})\s+')
KERNEL_DIR_REGEX = re.compile('\[DIR\]"> <a href="(\w+)\/')
HISTORY_FILE_REGEX = '^\w+\s+(\w+\s+\d+\s+\d+:\d+:\d+)\s+\w+\s+(\d+)\s+([0-9a-zA-Z\._\-]+)$'
CHRONOS_KERNEL_DIRECTORY_REGEX = '\$KERNELS\/(\w+)\/\w+'
PATH_VALUES_FIELD_REGEX = 'PATH_VALUES'
PATH_SYMBOLS_FIELD_REGEX = 'PATH_SYMBOLS'
PATH_VALUES_REGEX = r'(\s*(\'|"))([\/_0-9a-zA-Z-\.]*)(\'|")'


def __get_data_from_latest_chronos_setup_files(latest_chronos_setup_files, updated_mission):
    """
    Gets the latest kernels and chronos setup contents from NAIF. Ignores any LMST chronos setup
    files since these will be a subset of the other chronos setup files.
    :type latest_chronos_setup_files: list
    :type updated_mission: str
    :rtype: tuple
    """
    latest_chronos_setup_kernels = []
    latest_chronos_setup_contents = []

    non_lmst_setup_count = 0

    for file in latest_chronos_setup_files:
        data = urlopen(CHRONOS_DIRECTORY.format(updated_mission) + file)
        path_values, path_symbols, kernels_to_load, spacecraft_id, lmst_sclk_id, lmst_file = \
            __get_kernels_from_chronos_setup_contents(data)

        if not lmst_file:
            non_lmst_setup_count += 1
            latest_chronos_setup_kernels = kernels_to_load
            latest_chronos_setup_contents = urlopen(CHRONOS_DIRECTORY.format(updated_mission) + file).read().decode('utf-8').split('\n')

    if non_lmst_setup_count > 1:
        raise ValueError('Error finding latest chronos setup files from NAIF server. Found multiple '
                         'non-lmst chronos setup files uploaded within an hour of each other: {}'.format(
            str(latest_chronos_setup_files)))

    elif non_lmst_setup_count == 0:
        raise ValueError('Error finding latest chronos setup files from NAIF server. Could not find any non-lmst '
                         'chronos setup files.')

    return latest_chronos_setup_kernels, latest_chronos_setup_contents


def __create_new_chronos_setup(chronos_setup_contents, output_path):
    """
    Writes a chronos setup file based on the input contents but updates the paths
    to use the new directory structure from __create_kernel_directory_structure.
    :type chronos_setup_contents: list
    :type output_path: str
    :rtype: None
    """
    updated_contents = []
    in_path_values = False

    for line in chronos_setup_contents:
        if re.search(PATH_VALUES_FIELD_REGEX, line):
            in_path_values = True

        if re.search(PATH_SYMBOLS_FIELD_REGEX, line):
            in_path_values = False

        if in_path_values and re.search(PATH_VALUES_REGEX, line):
            regex_match = re.search(PATH_VALUES_REGEX, line)
            updated_contents.append(regex_match.group(1) + '../kernels/' + regex_match.group(4))

        else:
            updated_contents.append(line)

    with open(output_path, 'w') as f:
        f.write('\n'.join(updated_contents))


def __download_kernels(chronos_kernels, updated_mission, print_progress_bar=False):
    """
    Downloads the input kernels and corresponding chronos setup file and creates a directory
    structure for them. Creates a progress bar if specified.
    :type chronos_kernels: list
    :type updated_mission: str
    :type print_progress_bar: bool
    :rtype: None
    """
    # Initial call to print 0% progress
    if print_progress_bar:
        progress_bar(0, len(chronos_kernels))

    kernel_basename_lengths = [len(os.path.basename(kernel)) for kernel in chronos_kernels]
    longest_kernel_name = max(kernel_basename_lengths)

    for i, kernel in enumerate(chronos_kernels):
        url = kernel.replace('$KERNELS', KERNEL_BASE_DIRECTORY.format(updated_mission))
        output_path = kernel.replace('$KERNELS/', updated_mission + '/kernels/')

        if print_progress_bar:
            progress_bar(i, len(chronos_kernels), '{}/{} Downloading {:<{}s}'.format(i, len(chronos_kernels), os.path.basename(kernel), longest_kernel_name))

        __download_file(url, output_path)

    longest_message = '{}/{} Downloading {:<{}s}'.format(len(chronos_kernels), len(chronos_kernels), '', longest_kernel_name)

    if print_progress_bar:
        progress_bar(len(chronos_kernels), len(chronos_kernels), '{:<{}s}'.format(' ', len(longest_message)))


def __download_file(url, output_path):
    """
    Downloads a file from the input url and writes it to the given output path.
    :type url: str
    :type output_path: str
    :rtype: None
    """
    data = urlopen(url).read()
    with open(output_path, 'wb') as f:
        f.write(data)


def __get_chronos_kernel_directories(chronos_kernels):
    """
    Creates a list of kernel subdirectories from the chronos setup kernels.
    :type chronos_kernels: list
    :rtype: list
    """
    kernel_dirs = []
    for kernel in chronos_kernels:
        regex_match = re.search(CHRONOS_KERNEL_DIRECTORY_REGEX, kernel)
        if regex_match:
            dir = regex_match.group(1)
            if dir not in kernel_dirs:
                kernel_dirs.append(dir)

    return kernel_dirs


def __create_kernel_directory_structure(chronos_kernels, updated_mission):
    """
    Creates a directory structure for a chronos setup file and associated kernels.
    :type chronos_kernels: list
    :type updated_mission: str
    :rtype: None
    """
    __mkdir(updated_mission)
    __mkdir(updated_mission + '/setup')
    __mkdir(updated_mission + '/kernels')

    for kernel_dir in __get_chronos_kernel_directories(chronos_kernels):
        __mkdir(updated_mission + '/kernels/' + kernel_dir)


def __mkdir(dir):
    """
    Makes a directory if it has not been created, otherwise does nothing.
    :type dir: str
    :rtype: None
    """
    if not os.path.isdir(dir):
        os.mkdir(dir)


def __get_latest_file_url_from_history_file(history_file_url):
    """
    Parses the history file with the given url and returns the url of the latest kernel listed.
    :type history_file_url: str
    :rtype: str
    :return: url of latest file from history file
    """
    data = urlopen(history_file_url)
    lines = [str(l.decode('utf-8')) for l in data]
    files_and_times = []

    for line in lines:
        regex_match = re.search(HISTORY_FILE_REGEX, line)
        if regex_match:
            files_and_times.append(
                {'file': regex_match.group(3),
                 'updated': datetime.strptime(regex_match.group(2) + ' ' + regex_match.group(1), '%Y %b %d %H:%M:%S')
                 })

    return os.path.dirname(history_file_url) + '/' + max(files_and_times, key=lambda f: f['updated'])['file']


def __check_for_history_file(kernel, updated_mission):
    """
    Checks if there is a .history file for the input kernel. Returns the latest file url from
    the .history file if it exists, otherwise returns none.
    :type kernel: str
    :type updated_mission: str
    :rtype: str
    """
    history_file_url = kernel.replace('$KERNELS', KERNEL_BASE_DIRECTORY.format(updated_mission)) + '.history'
    try:
        return __get_latest_file_url_from_history_file(history_file_url)
    except HTTPError:
        return None


def __get_latest_files_from_dict(files_and_times):
    """
    Takes in the latest files_and_times list of dicts and returns the latest files. Considers
    any files uploaded within an hour of each other to be at the same time.
    :type files_and_times: list of dicts
    :rtype: list of strings
    """
    latest_update = max([f['updated'] for f in files_and_times])
    latest_files = [f['file'] for f in files_and_times if abs(f['updated'] - latest_update) < timedelta(hours=1)]

    return latest_files


def __get_files_on_naif_page(url):
    """
    Takes in a url of a folder on the NAIF server and returns a list of dicts with all
    files and their corresponding updated times.
    :type url: str
    :rtype: list
    :return: list with [{'file': '', 'updated': <datetime>}]
    """
    response = urlopen(url)
    html = response.read().decode('utf-8')
    table = re.compile(NAIF_DATA_REGEX).findall(html)
    files_and_times = [{'file': r[0], 'updated': datetime.strptime(r[1], '%d-%b-%Y %H:%M')} for r in table]

    return files_and_times


def __get_latest_chronos_setup(updated_mission):
    """
    Returns the latest kernels and the contents of the latest chronos setup file
    from NAIF. Only supports missions with the chronos setup infrastructure on NAIF.
    :type updated_mission: str
    :rtype: tuple
    :return: latest_kernels, latest_chronos_contents
    """
    latest_chronos_setup_files = __get_latest_files_from_dict(
        __get_files_on_naif_page(CHRONOS_DIRECTORY.format(updated_mission)))
    latest_kernels, latest_chronos_contents = \
        __get_data_from_latest_chronos_setup_files(latest_chronos_setup_files, updated_mission)

    return latest_kernels, latest_chronos_contents


def __get_latest_kernels(mission):
    """
    Returns the latest kernels and the chronos setup contents from NAIF.
    :type mission: str or int
    :rtype: tuple
    :return: latest_kernels, latest_chronos_contents, updated_mission
    """
    if str(mission).upper() not in SUPPORTED_MISSIONS:
        raise ValueError('Error, input mission {} is not one of the supported missions for '
                         'downloading chronos setup and kernels:\n{}'.format(mission, '\n'.join(SUPPORTED_MISSIONS.keys())))

    updated_mission = SUPPORTED_MISSIONS[str(mission).upper()]
    latest_kernels, latest_chronos_contents = __get_latest_chronos_setup(updated_mission)
    return latest_kernels, latest_chronos_contents, updated_mission


def __local_kernel_matches_naif(local_kernel_path, naif_kernel_url):
    """
    Checks if a local kernel matches the input NAIF kernel url by comparing contents.
    Only works for text files.
    :type local_kernel_path: str
    :type naif_kernel_url: str
    :rtype: bool
    """
    try:
        local_kernel_contents = open(local_kernel_path, 'r').readlines()
        naif_kernel_data = urlopen(naif_kernel_url)
        naif_kernel_contents = [str(l.decode('utf-8')) for l in naif_kernel_data]

        return local_kernel_contents == naif_kernel_contents
    # if we can't read the files then they are not text files, so we have to make a temp file to compare binary files
    except UnicodeDecodeError:
        temp = tempfile.NamedTemporaryFile()
        naif_kernel_data = urlopen(naif_kernel_url).read()
        temp.write(naif_kernel_data)

        return filecmp.cmp(local_kernel_path, temp.name)


def __download_chronos_setup_and_kernels(mission, print_progress_bar=False):
    """
    Downloads the latest kernels from NAIF and creates a chronos setup file
    which points to them. Only missions which support the chronos setup
    infrastructure on NAIF are supported currently.
    :type mission: str or int
    :type print_progress_bar: bool
    :rtype: str
    :return: path to chronos setup file
    """
    latest_kernels, latest_chronos_contents, updated_mission = __get_latest_kernels(mission)
    chronos_setup_name = '{}/setup/chronos.{}'.format(updated_mission, updated_mission.lower())

    __create_kernel_directory_structure(latest_kernels,updated_mission)
    __create_new_chronos_setup(latest_chronos_contents, chronos_setup_name)
    __download_kernels(latest_kernels, updated_mission, print_progress_bar)

    return os.path.abspath(chronos_setup_name)


def __check_if_loaded_kernels_are_latest(loaded_kernels, mission):
    """
    Takes in the loaded kernels and mission. Mission can be input as a string for
    mission name or as an integer for spacecraft ID. Only missions which support the
    chronos setup infrastructure on NAIF are supported currently.
    :type loaded_kernels: list
    :type mission: str or int
    :rtype: list
    :return: list of missing kernels
    """
    latest_kernels, latest_chronos_contents, updated_mission = __get_latest_kernels(mission)

    loaded_kernel_basename_dict = {os.path.basename(k): k for k in loaded_kernels}

    missing_kernels = []

    # for each of the latest kernels, check if it is in the list of loaded kernels
    for kernel in latest_kernels:
        kernel_basename = os.path.basename(kernel)

        # check if there is a .history file
        # this will be the case for files which are overwritten on NAIF, such as m2020.tls or insight.tsc
        latest_file_url_from_history = __check_for_history_file(kernel, updated_mission)
        if latest_file_url_from_history:
            # if the original kernel name (msl.tsc for example) is in the list of loaded kernels, then we need
            # to compare its contents with the latest kernel on NAIF
            if kernel_basename in loaded_kernel_basename_dict:
                if not __local_kernel_matches_naif(loaded_kernel_basename_dict[kernel_basename], latest_file_url_from_history):
                    missing_kernels.append(os.path.basename(latest_file_url_from_history))

            # if the original kernel name is not in the list of loaded kernels, then check if the full name is in the list
            # if so then they match, if not then add it to the list of missing kernels
            else:
                if os.path.basename(latest_file_url_from_history) not in loaded_kernel_basename_dict:
                    missing_kernels.append(os.path.basename(latest_file_url_from_history))

        # if there is no .history file then we can just compare file names
        else:
            if kernel_basename not in loaded_kernel_basename_dict:
                missing_kernels.append(kernel_basename)

    return missing_kernels
