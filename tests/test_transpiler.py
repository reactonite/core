import os
import stat
import uuid
import shutil
import pytest

from reactonite.Transpiler import Transpiler
from reactonite.PropsMap import props_map
from reactonite.Helpers import create_dir

from file_vars import minimal_working_example
from file_vars import minimal_working_example_js
from file_vars import full_working_example
from file_vars import full_working_example_js


def create_random_tree(base_path, num_directories=3, num_files=5):
    # num_files in each directory including base_dir
    tree = []

    for i in range(num_files):
        random_file = str(uuid.uuid4())
        random_file = os.path.join(base_path, random_file)

        open(random_file, 'a').close()
        tree.append(random_file)

    for i in range(num_directories):
        random_dir = str(uuid.uuid4())
        dir_path = os.path.join(base_path, random_dir)
        create_dir(dir_path)

        for i in range(num_files):
            random_file = str(uuid.uuid4())
            random_file = os.path.join(dir_path, random_file)

            open(random_file, 'a').close()
            tree.append(random_file)

    return tree


def test_transpiler_copyStaticFolderToDest():
    test_dir = os.path.join(os.path.expanduser("~"),
                            "reactonite-test")
    src_dir = os.path.join(test_dir, "src")
    dest_dir = os.path.join(test_dir, "dest")
    src_static_dir = os.path.join(src_dir, "static")

    if os.path.isdir(src_dir):
        shutil.rmtree(src_dir)
    if os.path.isdir(dest_dir):
        shutil.rmtree(dest_dir)
    if os.path.isdir(src_static_dir):
        shutil.rmtree(dest_dir)

    create_dir(src_dir)
    create_dir(dest_dir)
    create_dir(src_static_dir)

    config = {
        "src_dir": src_dir,
        "static_dir": "static",
        "dest_dir": dest_dir,
        "project_name": "test-project"
    }

    transpiler = Transpiler(config, props_map, verbose=True)

    # Create random static files in src_dir
    tree = create_random_tree(src_static_dir)

    # Copy using transpiler
    transpiler.copyStaticFolderToDest()

    # Replace src to dest
    for i, t in enumerate(tree):
        t = t.split(os.sep)
        if t[-2] == "src":
            t[-2] = "dest{}src".format(os.sep)
        elif t[-3] == "src":
            t[-3] = "dest{}src".format(os.sep)
        tree[i] = "{}".format(os.sep).join(t)

    # Check all files/directories are copied over
    # as intended
    for t in tree:
        assert os.path.isfile(t)


def check_minumum_example_js(filepath):
    with open(filepath, 'r') as file:
        filecontents = file.read()
    return filecontents == minimal_working_example_js


def check_full_example_js(filepath):
    with open(filepath, 'r') as file:
        filecontents = file.read()
    return filecontents == full_working_example_js


def test_transpiler_transpileFile():
    test_dir = os.path.join(os.path.expanduser("~"),
                            "reactonite-test")
    src_dir = os.path.join(test_dir, "src")
    src_static_dir = os.path.join(src_dir, "static")
    dest_dir = os.path.join(test_dir, "dest")
    dest_src_dir = os.path.join(dest_dir, "src")

    if os.path.isdir(src_dir):
        shutil.rmtree(src_dir)
    if os.path.isdir(dest_dir):
        shutil.rmtree(dest_dir)

    create_dir(src_dir)
    create_dir(dest_dir)
    create_dir(dest_src_dir)

    config = {
        "src_dir": src_dir,
        "static_dir": src_static_dir,
        "dest_dir": dest_dir,
        "project_name": "test-project"
    }

    transpiler = Transpiler(config, props_map, verbose=True)

    init_file_non_html_path = os.path.join(src_dir,
                                           "index.js")

    # init_file is not a HTML file
    with pytest.raises(RuntimeError):
        transpiler.transpileFile(init_file_non_html_path)

    init_file_path = os.path.join(src_dir,
                                  "index.html")

    # init_file_path file does not exist
    with pytest.raises(RuntimeError):
        transpiler.transpileFile(init_file_path)

#     # Create empty file init_file_path
#     open(init_file_path, 'a').close()

#     # head tag missing
#     with pytest.raises(RuntimeError):
#         transpiler.transpileFile(init_file_path)

#     # Write just the head tag
#     with open(init_file_path, 'a') as file:
#         file.write("""
# <head>Test header</head>
# """)

#     # body tag missing
#     with pytest.raises(RuntimeError):
#         transpiler.transpileFile(init_file_path)

    # Minimum working example
    with open(init_file_path, 'w') as file:
        file.write(minimal_working_example)

    transpiler.transpileFile(init_file_path)

    # Check dest file is present with correct file name
    assert os.path.isfile(os.path.join(dest_src_dir,
                                       "index.js"))

    transpiler.transpileFile(init_file_path, is_init_html=True)
    dest_file_path = os.path.join(dest_src_dir, "App.js")
    assert os.path.isfile(dest_file_path)

    assert check_minumum_example_js(dest_file_path)

    # Minimum working example
    with open(init_file_path, 'w') as file:
        file.write(full_working_example)

    transpiler.transpileFile(init_file_path, is_init_html=True)

    assert os.path.isfile(dest_file_path)
    assert check_full_example_js(dest_file_path)
