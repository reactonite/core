import os
import stat
import json
import shutil
import pytest

from reactonite.NodeWrapper import NodeWrapper
from reactonite.Helpers import create_dir


def delete_dir(filepath):
    pass


def check_package_json(filepath, extra_packages=[]):
    required_packages = ["react", "react-dom", "react-scripts"]
    required_packages.extend(extra_packages)
    with open(filepath, 'r') as file:
        package = json.load(file)
    for dep in required_packages:
        if dep not in package["dependencies"]:
            return False
    return True


@pytest.mark.dependency()
def test_create_react_app():
    test_dir = os.path.join(os.path.expanduser("~"),
                            "reactonite-test")
    app_name = "test-app"

    create_dir(test_dir)

    node = NodeWrapper()
    node.create_react_app(app_name, "dist", test_dir)

    assert os.path.isdir(os.path.join(test_dir,
                                      "dist"))

    package_json_filepath = os.path.join(test_dir,
                                         "dist",
                                         "package.json")
    assert os.path.isfile(package_json_filepath)
    assert check_package_json(package_json_filepath)


@pytest.mark.dependency(depends=["test_create_react_app"])
def test_install():
    test_dir = os.path.join(os.path.expanduser("~"),
                            "reactonite-test")
    app_name = "dist"
    node = NodeWrapper()
    node.install(package_name='react-helmet',
                 working_dir=os.path.join(test_dir, app_name))

    package_json_filepath = os.path.join(test_dir,
                                         app_name,
                                         "package.json")
    assert check_package_json(package_json_filepath,
                              extra_packages=["react-helmet"])


@pytest.mark.dependency(depends=["test_create_react_app"])
def test_build():
    test_dir = os.path.join(os.path.expanduser("~"),
                            "reactonite-test")
    app_name = "dist"
    node = NodeWrapper()
    node.build(working_dir=os.path.join(test_dir, app_name))

    build_dir = os.path.join(test_dir,
                             app_name,
                             "build")
    static_dir = os.path.join(build_dir,
                              "static")

    assert os.path.isdir(build_dir)
    assert os.path.isdir(static_dir)
    assert os.path.isdir(os.path.join(static_dir,
                                      "css"))
    assert os.path.isdir(os.path.join(static_dir,
                                      "js"))
    assert os.path.isdir(os.path.join(static_dir,
                                      "media"))

    assert os.path.isfile(os.path.join(build_dir,
                                       "index.html"))
    assert os.path.isfile(os.path.join(build_dir,
                                       "manifest.json"))
    assert os.path.isfile(os.path.join(build_dir,
                                       "favicon.ico"))
    assert os.path.isfile(os.path.join(build_dir,
                                       "robots.txt"))


@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Cleanup a testing directory once we are finished."""

    def on_rm_error(func, path, exc_info):
        # path contains the path of the file that couldn't be removed
        # let's just assume that it's read-only and unlink it.
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)

    test_dir = os.path.join(os.path.expanduser("~"),
                            "reactonite-test")

    def remove_test_dir():
        shutil.rmtree(test_dir, onerror=on_rm_error)

    request.addfinalizer(remove_test_dir)
