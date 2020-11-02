import os
import subprocess


class node_wrapper:
    def __init__(self,
                 app_name,
                 working_dir="."):
        self.app_name = app_name
        self.working_dir = working_dir

    def create_react_app(self, rename_to=None):
        subprocess.run(["npx", "create-react-app", self.app_name],
                       shell=True,
                       cwd=self.working_dir)

        if rename_to is not None:
            src = os.path.join(self.working_dir, self.app_name)
            dest = os.path.join(self.working_dir, rename_to)
            os.rename(src, dest)
