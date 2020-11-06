import json
import os


def create_dir(path):
    """Creates directory at the given path if it doesn't exist.

    Parameters
    ----------
    path : str
        Path to directory which needs to be created.

    Raises
    ------
    RuntimeError
        Raised if directory can't be created.
    """

    if os.path.isdir(path):
        print("{} already exists. Skipping.".format(path))
        return

    os.makedirs(path)
    if not os.path.isdir(path):
        raise RuntimeError('Folder can not be created at ' + str(path))


def create_file(path):
    """Creates the file at the given path if it doesn't exist.

    Parameters
    ----------
    path : str
        Path to file which needs to be created.

    Raises
    ------
    RuntimeError
        Raised if file can't be created.
    """

    open(path, 'w').close()
    if not os.path.isfile(path):
        raise RuntimeError('File can not be created at ' + str(path))


def write_to_json_file(path, content):
    """Writes content to a json file at the given path. Raises
    exception if file not exists.

    Parameters
    ----------
    path : str
        Path to file where content will be dumped.
    content : dict
        Dictonary to be dumped into the file.

    Raises
    ------
    FileNotFoundError
        Raised if file doesn't exist.
    """

    if not os.path.isfile(path):
        raise FileNotFoundError('File can not be reached at ' + str(path))

    with open(path, 'w') as outfile:
        json.dump(content, outfile, indent=4, sort_keys=True)
