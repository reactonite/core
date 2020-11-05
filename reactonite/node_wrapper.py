import os
import subprocess


class node_wrapper:
    """Node wrapper to execute commands corresponding to node js using python.

    Attributes
    ----------
    app_name : str
        Name of rectonite app to be created.
    working_dir : str, optional
        Directory where the app needs to be generated,by default is "." which
        implies present working directory.

    Methods
    -------
    create_react_app(rename_to=None)
        Creates a new react app and renames it as specified.
    install(package_name=None)
        Installs the given package for npm.
    """

    def __init__(self,
                 app_name,
                 working_dir="."):
        self.app_name = app_name
        self.working_dir = working_dir

    def create_react_app(self, rename_to=None):
        """Creates a new react app and renames it as specified.

        Parameters
        ----------
        rename_to : str, optional
            Renames the created React app to this, by default None which
            implies same as app name
        """

        subprocess.run(["npx", "create-react-app", self.app_name, "--use-npm"],
                       shell=True,
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

        subprocess.run(["npm", "i", package_name, "--save"],
                       shell=True,
                       cwd=working_dir)
