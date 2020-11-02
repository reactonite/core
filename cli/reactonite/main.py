import os
import click
from reactonite.config import DEFAULTS

from reactonite.node_wrapper import node_wrapper
from reactonite.watcher import reactonite_watcher

def create_dir(path):
    os.makedirs(path)
    if not os.path.isdir(path):
        raise Exception('Folder can not be created at', path)

def create_file(path):
    open(path, 'w').close()
    if not os.path.isfile(path):
        raise Exception('File can not be created at', path)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('project-name')
def create_empty_project(project_name):

    #TODO: Check if project_name is valid

    # Create directory project_name/src
    project_dir = os.path.join(".", project_name)
    dist_dir = os.path.join(project_dir, DEFAULTS.DEST_DIR)
    src_dir = os.path.join(project_dir, DEFAULTS.SRC_DIR)

    static_dir = os.path.join(src_dir, DEFAULTS.STATIC_DIR)
    html_file_path = os.path.join(src_dir, DEFAULTS.HTML_FILE_PATH)

    config_file_path = os.path.join(project_dir, DEFAULTS.CONFIG_FILE_PATH)

    # Create working dir and static dir

    create_dir(project_dir)
    create_dir(dist_dir)
    create_dir(src_dir)
    create_dir(static_dir)

    # Create template index.html in src dir
    create_file(html_file_path)

    # Create template config.json in project dir
    create_file(config_file_path)

    # Create npm project
    npm = node_wrapper(project_name, working_dir=dist_dir)
    npm.create_react_app()

    # Transpile once


@cli.command()
@click.argument('watch_dir')
def watch(watch_dir):
    watcher = reactonite_watcher(watch_dir)
    watcher.start()
