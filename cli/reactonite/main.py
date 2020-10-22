import os
import click

from reactonite.node_wrapper import node_wrapper


@click.group()
def cli():
    pass


@cli.command()
@click.argument('project-name')
def create_empty_project(project_name):

    # Create directory project_name/src
    project_dir = os.path.join(".", project_name)
    react_working_dir = os.path.join(project_dir, "react_src")
    static_dir = os.path.join(project_dir, "static")

    # Path to index.html
    html_file_path = os.path.join(project_dir, "index.html")

    # Create working dir and static dir
    os.makedirs(react_working_dir)
    os.makedirs(static_dir)

    # Create template index.html in project dir
    open(html_file_path, 'a').close()

    # Create npm project
    npm = node_wrapper(project_name,
                       working_dir=react_working_dir)
    npm.create_react_app()

    # Transpile once
