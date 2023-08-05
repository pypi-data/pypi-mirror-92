import os
import re

from src.davil.paths import check_slash, file_name


def list_image_files(directory, sort_function=None):
    return list_files(directory, endings=('.png', '.bmp', '.jpeg'), sort_function=sort_function)


def list_files(directory, endings=None, sort_function=None, full_path=True):
    paths = []

    names = sorted(os.listdir(directory), key=sort_function)
    if endings is not None:
        names = filter(lambda x: x.endswith(endings), names)

    if full_path:
        for name in names:
            paths.append(check_slash(directory) + name)
        return paths
    else:
        return names


def list_dirs(directory, full_path=True):
    contents = list_files(directory=directory, full_path=True)
    dirs = list(filter(lambda x: os.path.isdir(x), contents))
    if full_path:
        return dirs
    else:
        return [file_name(x) for x in dirs]


def list_files_with_patterns(path, patterns, endings, regex=True, sort_function=None):
    path_lists = []
    files = list_files(path, endings=endings, sort_function=sort_function)

    for p in patterns:
        if regex:
            path_lists.append(list(filter(lambda x: p.match(x), files)))
        else:
            path_lists.append(list(filter(lambda x: p in x, files)))
    return path_lists


def scan_for_existing_folders(folder, name, delim='_'):
    """
    Check the contents of the specified folder for enumerated subfolders with specified name.
    Returns the path to the next folder in the enumeration.
    Naming scheme: 'name''delim'0, 'name''delim'1, 'name''delim'2, ...
    If no folder is present, the path to the first one will be returned.

    :param folder: Folder to search for subfolders.
    :param name: Name base of enumerated subfolders.
    :param delim: Delimiter between name and enumeration.
    :return: The path to the next folder in the eneumeration.
    """
    contents = list_dirs(folder, full_path=False)
    contents = list(filter(lambda x: x.startswith(name), contents))
    contents = [x.replace(name + delim, '') for x in contents]
    contents = list(filter(lambda x: re.match('^\\d*$', x), contents))

    if len(contents) == 0:
        return folder + '/' + name + delim + str(0)

    contents = [int(x) for x in contents]
    contents = list(sorted(contents))
    return folder + '/' + name + delim + str(contents[-1] + 1)


def collect_files(root, regex):
    paths = []
    for path, subdirs, files in os.walk(root):
        for file in files:
            if re.match(regex, file):
                paths.append(check_slash(path.replace('\\', '/')) + file)
    return paths


def mkdir_if_not_exists(*paths):
    for p in paths:
        if not os.path.exists(p):
            os.makedirs(p, exist_ok=True)
