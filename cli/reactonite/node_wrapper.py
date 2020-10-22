import subprocess


class node_wrapper:
    def __init__(self,
                 app_name,
                 working_dir="."):
        self.app_name = app_name
        self.working_dir = working_dir

    def create_react_app(self):
        subprocess.run(["npx", "create-react-app", self.app_name],
                       shell=True,
                       cwd=self.working_dir)
