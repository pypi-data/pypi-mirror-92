"""
These functions are used to parse the chronos config file which is used as
an optional input to find kernels from the command line.
"""

import os
import re


def __find_chronos_config_from_env():
    """
    Checks environment variables for anything including CHRONOS_SETUP
    and returns any environment variables values matching that as a list.
    :return: list of chronos config files
    :rtype: list
    """
    chronos_config_files = []
    for env in os.environ:
        if 'CHRONOS_SETUP' in env:
            if os.path.isfile(os.environ[env]):
                chronos_config_files.append(os.environ[env])

    return chronos_config_files


def __get_list_values(line, it):
    vals = ''
    while True:
        line_str = line.decode('utf-8') if isinstance(line, bytes) else line
        vals += line_str
        if ')' in line_str:
            break
        line = next(it)
    vals = vals[vals.find('(')+1:vals.find(')')]
    return vals.replace("'", '').replace(',', '').split()


def __get_kernels_from_chronos_setup_contents(chronos_setup_reader):
    """
    Takes in an iterator for the contents of a chronos setup file and returns the kernels,
    spacecraft id, etc.
    :param chronos_setup_reader:
    :rtype: tuple
    """
    description_regex = r'^\s*CHRONOS setup file'
    path_values__header_regex = r'^\s*PATH_VALUES'
    path_symbols_header_regex = r'^\s*PATH_SYMBOLS'
    kernels_to_load_header_regex = r'^\s*KERNELS_TO_LOAD'
    spacecraft_id_regex = r'^\s*SPACECRAFT_ID\s*=\s*(-[0-9]+)\s*$'

    path_values = []
    path_symbols = []
    kernels_to_load = []
    spacecraft_id = None
    lmst_sclk_id = None
    lmst_file = False

    for line in chronos_setup_reader:
        line_str = line.decode('utf-8') if isinstance(line, bytes) else line # need to do this for when we read directly from NAIF server
        if re.search(description_regex, line_str) and 'LMST' in line_str:
            lmst_file = True

        elif re.search(path_values__header_regex, line_str):
            path_values = __get_list_values(line_str, chronos_setup_reader)

        elif re.search(path_symbols_header_regex, line_str):
            path_symbols = __get_list_values(line_str, chronos_setup_reader)

        elif re.search(kernels_to_load_header_regex, line_str):
            kernels_to_load = __get_list_values(line_str, chronos_setup_reader)

        elif re.search(spacecraft_id_regex, line_str):
            if lmst_file:
                lmst_sclk_id = int(re.search(spacecraft_id_regex, line_str).group(1))
            else:
                spacecraft_id = int(re.search(spacecraft_id_regex, line_str).group(1))

    return path_values, path_symbols, kernels_to_load, spacecraft_id, lmst_sclk_id, lmst_file


def __parse_chronos_config_file(chronos_config_path):
    """
    Parses an input Chronos config file and returns the spacecraft id, lmst sclk id,
    and the kernel files to load. If multiple conflicting spacecraft ids are found
    then an error will be thrown. If the file has LMST in the description then
    it is assumed to be an LMST config file and the spacecraft id will be taken as
    the LMST ID.

    This assumes a standard format and correct numbers of inputs in the chronos config
    file, such as the same number of entries in the PATH_VALUES and PATH_SYMBOLS.

    :param chronos_config_path: path to a chronos setup file
    :type chronos_config_path: str
    :return: spacecraft id, lmst sclk id, kernel list
    :rtype: tuple
    """
    # read the file and loop through
    with open(chronos_config_path) as fh:
        path_values, path_symbols, kernels_to_load, spacecraft_id, lmst_sclk_id, lmst_file = \
            __get_kernels_from_chronos_setup_contents(iter(fh.readlines()))

    # verify that the path values and symbols are the same length
    if len(path_values) != len(path_symbols):
        raise ValueError('Error parsing Chronos config file {}. The path values and path symbols '
                         'lists were not the same length.'.format(chronos_config_path))

    path_values_and_symbols = [{'symbol': path_symbols[i], 'value': path_values[i]} for i in range(0, len(path_symbols))]

    # now that we know they are the same length, loop through kernels and update them
    # we want to replace $KERNEL with /../kernels/etc.
    path_values_and_symbols.sort(key=lambda x: len(x['symbol']), reverse=True) # sort in reverse to support $KERNELS/$KERNELS_1/$1_KERNELS
    for i in range(0, len(path_values)):
        replacement_symbol  = '$' + path_values_and_symbols[i]['symbol']
        new_value           = path_values_and_symbols[i]['value']

        for j in range(0, len(kernels_to_load)):
            kernels_to_load[j] = kernels_to_load[j].replace(replacement_symbol, new_value)

    # for any relative paths, add the path to the chronos config file to the path
    chronos_config_dir = os.path.dirname(chronos_config_path)
    for i in range(0, len(kernels_to_load)):
        kernels_to_load[i] = update_relative_path(kernels_to_load[i], chronos_config_dir)

    # return the values that we captured
    return spacecraft_id, lmst_sclk_id, kernels_to_load


def update_relative_path(absolute_or_relative_path, path_to_prepend):
    """
    If the input path is relative then the path_to_prepend will be added in front of it.
    :type absolute_or_relative_path: str
    :type path_to_prepend: str
    :rtype: str
    """
    if os.path.isabs(absolute_or_relative_path):
        return absolute_or_relative_path

    return os.path.join(path_to_prepend, absolute_or_relative_path)


def __get_spice_inputs_from_chronos_files(chronos_config_path=None):
    """
    Optionally takes in the path to a chronos config file and parses it to find
    all kernels to load. If a path is not provided then this function will look
    for the file using CHRONOS environment variables.

    For LMST, if an lmst sclk id is not found in the chronos config files
    then the default will be the spacecraft id * 1000 + 900. For example,
    InSight will have spacecraft id = -189 and lmst sclk id = -189900. If the
    spacecraft is not on the surface of mars then the LMST sclk id will have
    no effect, but will still be set.

    :param chronos_config_path: path to chronos config
    :type chronos_config_path: str
    :return: None
    """
    # if provided, get the values from it
    if chronos_config_path:
        chronos_config_files = [chronos_config_path]
    else:
        chronos_config_files = __find_chronos_config_from_env()

    spacecraft_ids = []
    lmst_sclk_ids = []
    all_kernels = []

    # loop through each file and store off values
    for chronos_config_file in chronos_config_files:
        spacecraft_id, lmst_sclk_id, kernels = __parse_chronos_config_file(chronos_config_file)
        if spacecraft_id:
            spacecraft_ids.append(spacecraft_id)
        if lmst_sclk_id:
            lmst_sclk_ids.append(lmst_sclk_id)
        if kernels:
            all_kernels += kernels

    # take the set of each list and complain if there were multiple ids
    filtered_spacecraft_ids = list(set(spacecraft_ids))
    filtered_lmst_sclk_ids = list(set(lmst_sclk_ids))
    all_kernels = set(all_kernels)

    if not chronos_config_files:
        raise ValueError('Error: Could not find any chronos config files to load. '
                         'Check CHRONOS_SETUP environment variables.')

    if len(filtered_spacecraft_ids) == 0:
        raise ValueError('Error parsing chronos config files. Could not find a valid spacecraft id '
                         'in these files: {}'.format(', '.join(chronos_config_files)))

    if len(filtered_spacecraft_ids) > 1:
        raise ValueError('Error parsing chronos config files. Multiple spacecraft ids were found '
                         'when only one was expected: {}\nThese config files were parsed: {}'.format(
            ', '.join(filtered_spacecraft_ids), ', '.join(chronos_config_files)))

    if len(filtered_lmst_sclk_ids) > 1:
        raise ValueError('Error parsing chronos config files. Multiple LMST SCLK ids were found '
                         'when only one was expected: {}\nThese config files were parsed: {}'.format(
            ', '.join(filtered_lmst_sclk_ids), ', '.join(chronos_config_files)))

    if len(all_kernels) == 0:
        raise ValueError('Error parsing chronos config files. No kernels could be found in these '
                         'config files: {}'.format(', '.join(chronos_config_files)))

    # now that we know everything is a valid length, assign the values appropriately
    spacecraft_id = filtered_spacecraft_ids[0]

    if len(filtered_lmst_sclk_ids) == 0:
        lmst_sclk_id = int(str(spacecraft_id) + '900')

    else:
        lmst_sclk_id = filtered_lmst_sclk_ids[0]

    return spacecraft_id, lmst_sclk_id, all_kernels
