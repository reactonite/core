import os
import sys
from distutils.dir_util import copy_tree

import click

from reactonite.config import DEFAULTS
from reactonite.node_wrapper import node_wrapper
from reactonite.transpiler import Transpiler
from reactonite.watcher import reactonite_watcher


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


@click.group()
def cli():
    """Entry point for reactonite cli."""

    pass


@cli.command()
@click.argument('project-name')
def create_project(project_name):
    """Command for creating new reactonite project from scratch.

    Creates a new reactonite project with given PROJECT_NAME and installs npm
    packages along with basic directory structure layout.

    Parameters
    ----------
    project_name : str
        Name of the project to be created.

    Raises
    ------
    RuntimeError
        If project name is invalid.
    """

    # Valid project name checks
    if not project_name.islower():
        raise RuntimeError(
            "Invalid project name " +
            str(project_name) +
            " must be lower case."
        )

    if any(c != '-' and not c.isalnum() for c in project_name):
        raise RuntimeError(
            "Invalid project name " +
            str(project_name) +
            " only - is allowed as a special character."
        )

    project_dir = os.path.join(".", project_name)

    if os.path.exists(project_dir):
        raise RuntimeError(
            "Invalid project name " +
            str(project_name) +
            " directory already exists."
        )

    dist_dir = os.path.join(project_dir, DEFAULTS.DEST_DIR)
    dist_src_dir = os.path.join(dist_dir, DEFAULTS.SRC_DIR)
    dist_static_dir = os.path.join(dist_src_dir, DEFAULTS.STATIC_DIR)

    src_dir = os.path.join(project_dir, DEFAULTS.SRC_DIR)

    src_static_dir = os.path.join(src_dir, DEFAULTS.STATIC_DIR)
    html_file_path = os.path.join(src_dir, DEFAULTS.HTML_FILE_PATH)

    config_file_path = os.path.join(project_dir, DEFAULTS.CONFIG_FILE_PATH)

    # Create project directory
    create_dir(project_dir)

    # Initial setup of project/src directory
    package_path = os.path.dirname(sys.modules[__name__].__file__)
    init_src_dir_path = os.path.join(package_path, DEFAULTS.INIT_FILES_DIR)
    copy_tree(init_src_dir_path, src_dir)

    # Create template config.json in project dir
    create_file(config_file_path)

    # Create react app
    npm = node_wrapper(project_name,
                       working_dir=project_dir)
    npm.create_react_app(rename_to=DEFAULTS.DEST_DIR)

    # Install NPM packages
    npm.install(package_name='react-helmet', working_dir=dist_dir)

    # Transpile once
    transpiler = Transpiler(src_dir,
                            html_file_path,
                            src_static_dir,
                            dist_dir,
                            dist_src_dir,
                            dist_static_dir,
                            parser=DEFAULTS.BS_PARSER,
                            verbose=True)
    transpiler.transpile()


@cli.command()
@click.argument('watch_dir')
def watch(watch_dir):
    """Command for watching for changes and initializing the watcher.

    Starts watching for changes in the specified project directory.

    Parameters
    ----------
    watch_dir : str
        Path of directory to be watched for changes.
    """

    watcher = reactonite_watcher(watch_dir)
    watcher.start()
