import os
import click
from reactonite.config import DEFAULTS

from reactonite.node_wrapper import node_wrapper
from reactonite.watcher import reactonite_watcher
from reactonite.transpiler import Transpiler


def init_html_file(filepath):
    with open(filepath, 'w') as file:
        file.write(
            """
<!doctype html>
<html>

<head>
<title>This is the title of the webpage!</title>
</head>

<body>
<p>This is example statement. Anything inside the <strong>body</strong> tag will appear on the page, just
    like this
    <strong>p</strong> tag and it contents.</p>
</body>

</html>
            """
        )


def create_dir(path):
    if os.path.isdir(path):
        print("{} already exists. Skipping.".format(path))
        return

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
def create_project(project_name):

    # TODO: Check if project_name is valid

    # Create directory project_name/src
    project_dir = os.path.join(".", project_name)

    dist_dir = os.path.join(project_dir, DEFAULTS.DEST_DIR)
    dist_src_dir = os.path.join(dist_dir, DEFAULTS.SRC_DIR)
    dist_static_dir = os.path.join(dist_dir, DEFAULTS.STATIC_DIR)

    src_dir = os.path.join(project_dir, DEFAULTS.SRC_DIR)

    src_static_dir = os.path.join(src_dir, DEFAULTS.STATIC_DIR)
    html_file_path = os.path.join(src_dir, DEFAULTS.HTML_FILE_PATH)

    config_file_path = os.path.join(project_dir, DEFAULTS.CONFIG_FILE_PATH)

    # Create working dir and static dir
    create_dir(project_dir)
    create_dir(src_dir)
    create_dir(src_static_dir)

    # Create template index.html in src dir
    create_file(html_file_path)
    init_html_file(html_file_path)

    # Create template config.json in project dir
    create_file(config_file_path)

    # Create npm project
    npm = node_wrapper(project_name,
                       working_dir=project_dir)
    npm.create_react_app(rename_to=DEFAULTS.DEST_DIR)

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
    watcher = reactonite_watcher(watch_dir)
    watcher.start()
