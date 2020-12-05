import os
import subprocess


class NodeWrapper:
    """Node wrapper to execute commands corresponding to node js using python.

    Attributes
    ----------
    npx : str
        Commandline to be used for npx according to system(Linux, Windows)
    npm : str
        Commandline to be used for npm according to system(Linux, Windows)
    node : str
        Commandline to be used for node according to system(Linux, Windows)
    """

    def __init__(self):

        if os.name == "nt":
            self.npx = "npx.cmd"
            self.npm = "npm.cmd"
            self.node = "node.exe"
        else:
            self.npx = "npx"
            self.npm = "npm"
            self.node = "node"

        self.check_react_install()

    def check_react_install(self):
        """Checks the installation of Nodejs/npm/npx. If npm is not
        available it throws an error.

        Raises
        ------
        RuntimeError
            Raised if Nodejs/npm/npx is not available.
        """

        try:
            subprocess.run([self.npx, "--version"],
                           shell=False,
                           cwd='.',
                           stdout=subprocess.DEVNULL)
        except Exception:
            raise RuntimeError("npx not found. Please install/reinstall node")

        try:
            subprocess.run([self.npm, "--version"],
                           shell=False,
                           cwd='.',
                           stdout=subprocess.DEVNULL)
        except Exception:
            raise RuntimeError("npm not found. Please install/reinstall node")

        try:
            subprocess.run([self.node, "--version"],
                           shell=False,
                           cwd='.',
                           stdout=subprocess.DEVNULL)
        except Exception:
            raise RuntimeError("nodejs not found. Please install/reinstall \
                node")

        # TODO: Log these version numbers

    def create_react_app(self, project_name, rename_to=None, working_dir='.'):
        """Creates a new react app and renames it as specified.

        Parameters
        ----------
        project_name : str
            Project name to be used to create the app
        rename_to : str
            Renames the created React app to this
        working_dir : str
            Working dir to run commands inside
        """

        subprocess.run([self.npx, "create-react-app",
                        project_name, "--use-npm"],
                       shell=False,
                       cwd=working_dir)

        src = os.path.join(working_dir, project_name)
        if rename_to is not None:
            dest = os.path.join('.', rename_to)
            os.rename(src, dest)

    def install(self, package_name, working_dir):
        """Installs the given package in npm and saves in package.json

        Parameters
        ----------
        package_name : str
            Package to be installed.
        working_dir : str
            Directory containing npm project root
        """

        subprocess.run([self.npm, "i", package_name, "--save"],
                       shell=False,
                       cwd=working_dir)

    def start(self, working_dir):
        """Runs the command npm start in the given working directory

        Parameters
        ----------
        working_dir : str
            Directory to execute the command in.
        """

        subprocess.run([self.npm, "start"],
                       shell=False,
                       cwd=working_dir)

    def build(self, working_dir):
        """Create an optimized build of your app in the build folder

        Parameters
        ----------
        working_dir : str
            Directory containing npm project root
        """

        subprocess.run([self.npm, "run", "build"],
                       shell=False,
                       cwd=working_dir)

    def prettify(self, path, working_dir="."):
        """Runs code formatting using prettier on the given path

        Parameters
        ----------
        path : str
            Filepath or directory to run prettier on
        working_dir : str
            Directory from which command is run
        """

        subprocess.run([self.npx, "prettier", "--write", path],
                       shell=False,
                       cwd=working_dir)
