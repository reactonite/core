import json
import os
import sys
from distutils.dir_util import copy_tree

import click

from .config import DEFAULTS
from .helpers import create_dir, create_file, write_to_json_file
from .node_wrapper import NodeWrapper
from .transpiler import Transpiler
from .watcher import ReactoniteWatcher


@click.group()
def cli():
    """Entry point for Reactonite cli."""

    pass


@cli.command()
@click.argument('project-name')
def create_project(project_name):
    """Command for creating new Reactonite project from scratch.

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

    CONSTANTS = DEFAULTS()

    project_dir = os.path.join(".", project_name)
    dest_dir = os.path.join(project_dir, CONSTANTS.DEST_DIR)
    src_dir = os.path.join(project_dir, CONSTANTS.SRC_DIR)

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

    if os.path.exists(project_dir):
        raise RuntimeError(
            "Invalid project name " +
            str(project_name) +
            " directory already exists."
        )

    config_file_path = os.path.join(project_dir, CONSTANTS.CONFIG_FILE_NAME)
    config_settings = {
        "src_dir": CONSTANTS.SRC_DIR,
        "dest_dir": CONSTANTS.DEST_DIR
    }

    # Create project directory
    create_dir(project_dir)

    # Initial setup of project/src directory
    package_path = os.path.dirname(sys.modules[__name__].__file__)
    init_src_dir_path = os.path.join(package_path, CONSTANTS.INIT_FILES_DIR)
    copy_tree(init_src_dir_path, src_dir)

    # Create template config.json in project dir
    create_file(config_file_path)
    write_to_json_file(
        config_file_path,
        content=config_settings
    )

    # Create react app
    npm = NodeWrapper(project_name, working_dir=project_dir)
    npm.create_react_app(rename_to=CONSTANTS.DEST_DIR)

    # Install NPM packages
    npm.install(package_name='react-helmet', working_dir=dest_dir)

    # Transpile once
    transpiler = Transpiler({
        "src_dir": src_dir,
        "dest_dir": dest_dir
    }, verbose=True)

    transpiler.transpile_project()


@cli.command()
@click.option('--verbose', '-v', is_flag=True)
def transpile_project(verbose):
    """Command for transpiling a Reactonite project built using
    create-project commandline.

    Parameters
    ----------
    verbose : bool, optional
        Verbosity of the command

    Raises
    ------
    File
        If project name is invalid.
    """

    CONSTANTS = DEFAULTS()
    config_file = CONSTANTS.CONFIG_FILE_NAME

    if not os.path.exists(config_file):
        raise FileNotFoundError(
            "Reactonite config.json file doesn't exist, can't proceed."
        )

    with open(config_file) as infile:
        config_settings = json.load(infile)

    transpiler = Transpiler(config_settings, verbose=verbose)
    transpiler.transpile_project()


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

    watcher = ReactoniteWatcher(watch_dir)
    watcher.start()
