import json
import os


def get_parent_dir(path):
    """Returns location of the parent directory for a given path.

    Parameters
    ----------
    path : str
        Path of the file or folder for which we need the parent directory.

    Returns
    -------
    str
        Location of the parent directory
    """
    pdir = os.path.dirname(path)
    if not pdir:
        pdir = '.'
    return pdir


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

    pdir = get_parent_dir(path)
    if os.access(pdir, os.W_OK):
        open(path, 'w').close()
        if not os.path.isfile(path):
            raise RuntimeError('File can not be created at ' + str(path))
    else:
        raise RuntimeError(
            'Not enough permissions to create file at ' +
            str(pdir)
        )


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
    RuntimeError
        Raised if not enough permissions to write in file
    """

    if os.access(path, os.W_OK):
        if not os.path.isfile(path):
            raise FileNotFoundError('File can not be reached at ' + str(path))

        with open(path, 'w') as outfile:
            json.dump(content, outfile, indent=4, sort_keys=True)
    else:
        raise RuntimeError('Not enough permissions to write at ' + str(path))
