import os
import sys
from distutils.dir_util import copy_tree
import _thread

import click

from .Constants import DEFAULTS
from .Helpers import create_dir
from .NodeWrapper import NodeWrapper
from .ReactoniteWatcher import ReactoniteWatcher
from .Transpiler import Transpiler
from .Config import Config


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
    config_settings = Config(config_file_path)
    config_settings.add_to_config("src_dir", CONSTANTS.SRC_DIR)
    config_settings.add_to_config("dest_dir", CONSTANTS.DEST_DIR)
    config_settings.add_to_config("project_name", project_name)

    # Create project directory
    create_dir(project_dir)

    # Initial setup of project/src directory
    package_path = os.path.dirname(sys.modules[__name__].__file__)
    init_src_dir_path = os.path.join(package_path, CONSTANTS.INIT_FILES_DIR)
    copy_tree(init_src_dir_path, src_dir)

    # Create template config.json in project dir
    config_settings.save_config()

    # Create react app
    npm = NodeWrapper(project_name, working_dir=project_dir)
    npm.create_react_app(rename_to=CONSTANTS.DEST_DIR)

    # Install NPM packages
    npm.install(package_name='react-helmet', working_dir=dest_dir)

    # Transpile once
    transpiler = Transpiler({
        "src_dir": src_dir,
        "dest_dir": dest_dir
        },
        props_map=CONSTANTS.PROPS_MAP,
        verbose=True
    )

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
    FileNotFoundError
        If config.json file doesn't exist.
    """

    CONSTANTS = DEFAULTS()
    config_file = CONSTANTS.CONFIG_FILE_NAME
    config_settings = Config(config_file, load=True)

    transpiler = Transpiler(
        config_settings.get_config(),
        props_map=CONSTANTS.PROPS_MAP,
        verbose=verbose
    )
    transpiler.transpile_project()


@cli.command()
def start():
    """Command to start realtime development transpiler for Reactonite.

    Starts watching for changes in project directory and transpiles codebase.

    Raises
    ------
    FileNotFoundError
        If config.json file doesn't exist.
    """

    CONSTANTS = DEFAULTS()
    config_file = CONSTANTS.CONFIG_FILE_NAME
    config_settings = Config(config_file, load=True)

    dest_dir = config_settings.get("dest_dir")

    npm = NodeWrapper()
    watcher = ReactoniteWatcher(config_settings.get_config())

    try:
        _thread.start_new_thread(npm.start, (os.path.join(".", dest_dir),))
    except Exception:
        print("Error: unable to start thread")
    watcher.start()


@cli.command()
def build():
    """Command to start realtime development transpiler for Reactonite.

    Starts watching for changes in project directory and transpiles codebase.

    Raises
    ------
    FileNotFoundError
        If config.json file doesn't exist.
    """

    CONSTANTS = DEFAULTS()
    config_file = CONSTANTS.CONFIG_FILE_NAME
    config_settings = Config(config_file, load=True)

    npm = NodeWrapper(config_settings.get("project_name"),
                      working_dir=config_settings.get("dest_dir"))
    npm.build()

    # Move build folder to project_dir instead of dest_dir
    npm_build = os.path.join(config_settings.get("dest_dir"), "build")
    project_build = os.path.join(".", "build")
    os.rename(npm_build, project_build)
