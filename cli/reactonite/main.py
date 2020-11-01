import os
import click
from reactonite.config import DEFAULTS

from reactonite.node_wrapper import node_wrapper


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
    os.makedirs(dist_dir)
    # TODO: Check if directory created
    os.makedirs(src_dir)
    # TODO: Check if directory created
    os.makedirs(static_dir)
    # TODO: Check if directory created

    # Create template index.html in src dir
    open(html_file_path, 'a').close()
    # TODO: Check if file created

    # Create template config.json in project dir
    open(config_file_path, 'a').close()
    # TODO: Check if file created

    # Create npm project
    npm = node_wrapper(project_name,
                       working_dir=dist_dir)
    npm.create_react_app()

    # Transpile once
