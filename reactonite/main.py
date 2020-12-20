import _thread
import os
import sys
from distutils.dir_util import copy_tree

import click

from .Config import Config
from .Constants import DEFAULTS
from .Helpers import create_dir
from .NodeWrapper import NodeWrapper
from .ReactoniteWatcher import ReactoniteWatcher
from .Transpiler import Transpiler

from reactonite import __version__
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/grapesjs', methods=['POST'])
def fetchCodeFromGrapesjs():
    if request.method == 'POST':
        try:
            # print(request.form['html'])
            # print(request.form['css'])
            data = {'Status': 'Data Received Successfully'}
            return make_response(jsonify(data), 200)
        except Exception as e:
            print('Error in handling POST Request - ', e)
            data = {'Status': 'Error in Handling POST Request',
                    'Error': str(e)}
            return make_response(jsonify(data), 550)

@click.group()
@click.version_option(__version__)
@click.pass_context
def cli(ctx):
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
    config_settings.add_to_config("project_name", project_name)
    config_settings.add_to_config("src_dir", CONSTANTS.SRC_DIR)
    config_settings.add_to_config("dest_dir", CONSTANTS.DEST_DIR)

    # Create project directory
    create_dir(project_dir)

    # Initial setup of project/src directory
    package_path = os.path.dirname(sys.modules[__name__].__file__)
    init_src_dir_path = os.path.join(package_path, CONSTANTS.INIT_FILES_DIR)
    copy_tree(init_src_dir_path, src_dir)

    # Move .gitignore to outerlayer
    gitignore_src = os.path.join(src_dir, '.gitignore')
    gitignore_dest = os.path.join(project_dir, '.gitignore')
    os.rename(gitignore_src, gitignore_dest)

    # Create template config.json in project dir
    config_settings.save_config()

    # Transpile once
    transpiler = Transpiler(
        config_settings.get_config(),
        props_map=CONSTANTS.PROPS_MAP,
        verbose=True,
        create_project=True
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
    """Command to start realtime development transpiler for Reactonite. It
    starts react development server in a seperate thread as well and watches
    for changes in project directory and transpiles codebase.

    Raises
    ------
    FileNotFoundError
        If config.json file doesn't exist
    RuntimeError
        If ReactJs development thread is not able to start
    """

    CONSTANTS = DEFAULTS()
    config_file = CONSTANTS.CONFIG_FILE_NAME
    config_settings = Config(config_file, load=True)
    dest_dir = config_settings.get("dest_dir")
    # Initial transpile
    transpiler = Transpiler(
        config_settings.get_config(),
        props_map=CONSTANTS.PROPS_MAP,
        verbose=True
    )
    transpiler.transpile_project()

    npm = NodeWrapper()
    watcher = ReactoniteWatcher(config_settings.get_config())

    try:
        _thread.start_new_thread(npm.start, (os.path.join(".", dest_dir),))
    except Exception:
        raise RuntimeError("Unable to start ReactJs development thread")

    # Starting Watcher
    watcher.start()

@cli.command()
def start_gui():
    """Command to start realtime development transpiler and GUI for Reactonite. It
    starts react development server and GUI in a seperate thread as well and watches
    for changes in project directory and transpiles codebase.

    Raises
    ------
    FileNotFoundError
        If config.json file doesn't exist
    RuntimeError
        If ReactJs development thread is not able to start
    """

    CONSTANTS = DEFAULTS()
    config_file = CONSTANTS.CONFIG_FILE_NAME
    config_settings = Config(config_file, load=True)
    dest_dir = config_settings.get("dest_dir")
    # Initial transpile
    transpiler = Transpiler(
        config_settings.get_config(),
        props_map=CONSTANTS.PROPS_MAP,
        verbose=True
    )
    transpiler.transpile_project()

    npm = NodeWrapper()
    watcher = ReactoniteWatcher(config_settings.get_config())

    try:
        _thread.start_new_thread(npm.start, (os.path.join(".", dest_dir),))
    except Exception:
        raise RuntimeError("Unable to start ReactJs development thread")

    # Starting Flask Server
    app.run(port=5000)

    # Starting Watcher
    watcher.start()

@cli.command()
def build():
    """Command to get a static build of your app after transpilation.

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
        verbose=True
    )
    transpiler.transpile_project()

    dest_dir = config_settings.get("dest_dir")

    npm = NodeWrapper()
    npm.build(working_dir=dest_dir)

    # Move build folder to project_dir instead of dest_dir
    npm_build = os.path.join(dest_dir, "build")
    project_build = os.path.join(".", "build")

    os.rename(npm_build, project_build)
