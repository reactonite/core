import _thread
import os
import shutil
import sys
from distutils.dir_util import copy_tree
from threading import Thread

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

from .CreateHtmlCss import saveCss, saveHtml

app = Flask(__name__)
CORS(app)


@app.route('/grapesjs', methods=['POST'])
def fetchCodeFromGrapesjs():
    if request.method == 'POST':
        try:
            CONSTANTS = DEFAULTS()

            src_dir = CONSTANTS.SRC_DIR

            saveCss(request.form['css'], src_dir)
            saveHtml(request.form['html'], src_dir)

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
@click.argument('project-name')
def gui(project_name):
    """Command to start realtime development transpiler and GUI for Reactonite. It
    starts react development server and GUI in a seperate thread as well and
    watches for changes in project directory and transpiles codebase.

    Parameters
    ----------
    project_name : str
        Name of the project to be created.

    Raises
    ------
    FileNotFoundError
        If config.json file doesn't exist
    RuntimeError
        If ReactJs development thread is not able to start
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

    project_dir = os.path.join(".", project_name)

    os.chdir(project_dir)

    # src_dir = os.path.join(project_dir, CONSTANTS.SRC_DIR)
    src_dir = CONSTANTS.SRC_DIR

    folders = next(os.walk(src_dir))[1]
    files = next(os.walk(src_dir))[2]

    for folder in folders:
        shutil.rmtree(os.path.join(src_dir, folder))

    for file in files:
        if file != 'index.html':
            os.remove(os.path.join(src_dir, file))

    config_file_path = os.path.join(os.path.abspath('.'),
                                    CONSTANTS.CONFIG_FILE_NAME)

    print(config_file_path)

    config_settings = Config(config_file_path, load=True)

    dest_dir = config_settings.get("dest_dir")

    npm = NodeWrapper()
    watcher = ReactoniteWatcher(config_settings.get_config())

    npm.install_grapesjs(os.path.abspath('.'))

    try:
        reactonite_thread = Thread(target=npm.start,
                                   args=(os.path.join(".", dest_dir),))
        grapesjs_thread = Thread(target=npm.start_grapesjs,
                                 args=(os.path.abspath('.'),))
        grapesjs_thread.daemon = True
        flask_thread = Thread(target=app.run,
                              args=('localhost', 5000,))
        flask_thread.daemon = True
        watcher_thread = Thread(target=watcher.start,
                                args=())
        flask_thread.daemon = True

        try:
            flask_thread.start()
            grapesjs_thread.start()
            reactonite_thread.start()
            watcher_thread.start()

            reactonite_thread.join()
        except KeyboardInterrupt:
            try:
                sys.exit()
            except SystemExit:
                os._exit(0)

    except Exception:
        raise RuntimeError("Unable to start ReactJs development thread")


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
