import os
import click

from reactonite.node_wrapper import node_wrapper
from reactonite.watcher import reactonite_watcher


@click.group()
def cli():
    pass


@cli.command()
@click.argument('project-name')
def create_empty_project(project_name):

    # Create directory project_name/src
    project_dir = os.path.join(".", project_name)
    dist_dir = os.path.join(project_dir, "dist")
    src_dir = os.path.join(project_dir, "src")

    static_dir = os.path.join(src_dir, "static")
    html_file_path = os.path.join(src_dir, "index.html")

    config_file_path = os.path.join(project_dir, "config.json")

    # Create working dir and static dir
    os.makedirs(dist_dir)
    os.makedirs(src_dir)
    os.makedirs(static_dir)

    # Create template index.html in src dir
    open(html_file_path, 'a').close()

    # Create template config.json in project dir
    open(config_file_path, 'a').close()

    # Create npm project
    npm = node_wrapper(project_name,
                       working_dir=dist_dir)
    npm.create_react_app()

    # Transpile once


@cli.command()
@click.argument('watch_dir')
def watch(watch_dir):
    watcher = reactonite_watcher(watch_dir)
    watcher.start()
