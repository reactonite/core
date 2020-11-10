import os
import subprocess


class NodeWrapper:
    """Node wrapper to execute commands corresponding to node js using python.

    Attributes
    ----------
    app_name : str
        Name of rectonite app to be created.
    working_dir : str, optional
        Directory where the app needs to be generated,by default is "." which
        implies present working directory.
    """

    def __init__(self,
                 app_name,
                 working_dir="."):

        # TODO: Add docs for these and remove app_name and working_dir
        # to create_react_app
        self.app_name = app_name
        self.working_dir = working_dir

        if os.name == "nt":
            self.npx = "npx.cmd"
            self.npm = "npm.cmd"
        else:
            self.npx = "npx"
            self.npm = "npm"

    def create_react_app(self, rename_to=None):
        """Creates a new react app and renames it as specified.

        Parameters
        ----------
        rename_to : str, optional
            Renames the created React app to this, by default None which
            implies same as app name
        """

        subprocess.run([self.npx, "create-react-app",
                        self.app_name, "--use-npm"],
                       shell=False,
                       cwd=self.working_dir)

        if rename_to is not None:
            src = os.path.join(self.working_dir, self.app_name)
            dest = os.path.join(self.working_dir, rename_to)
            os.rename(src, dest)

    def install(self, package_name=None, working_dir=None):
        """Installs the given package in npm and saves in package.json

        Parameters
        ----------
        package_name : str
            Package to be installed.
        working_dir : str
            Directory to execute the command in.
        """

        subprocess.run([self.npm, "i", package_name, "--save"],
                       shell=False,
                       cwd=working_dir)