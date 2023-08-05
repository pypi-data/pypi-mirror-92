def file_name(path, delim='/'):
    split = path.split(delim)
    return split[-1]


def strip_ending(path_or_name: str):
    split = path_or_name.split('.')
    assert len(split) == 2
    return split[0]


def ending(path_or_name: str):
    split = path_or_name.split('.')
    assert len(split) == 2
    return '.' + split[1]


def folder(path_to_file, delim='/'):
    """
    Extract the folder path containing the file with specified path. Specified delimiter will be appended to the found
    folder path.

    :param path_to_file: Path to some file.
    :param delim: Path delimiter.
    :return: Path to folder containing specified file.
    """
    name = file_name(path=path_to_file, delim=delim)
    if '.' not in name:
        raise ValueError('Specified path: \'{}\' appears not to point to a file.'.format(path_to_file))
    split = path_to_file.split(delim)
    return delim.join(split[0:-1]) + delim


def check_slash(path):
    if path.endswith('/'):
        return path
    else:
        return path + '/'


def check_extension_dot(extension):
    if extension.startswith('.'):
        return extension
    else:
        return '.' + extension
