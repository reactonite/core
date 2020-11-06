import os
from distutils.dir_util import copy_tree

from bs4 import BeautifulSoup


class Transpiler:
    """Transpiler responsible for translating HTML code to React

    Attributes
    ----------
    src_dir : str
        Path of the source directory within the project directory
    dest_dir : str
        Path to the transpiled React app within the project directory
    parser : str, optional
        Specify which parser to use for reading HTML files, defaults
        to "html.parser"
    verbose : bool, optional
        Specify the verbosity of the transpiler, defaults to False
    """

    def __init__(self,
                 config_settings,
                 verbose=False):
        """Transpiler initiator takes config settings and unpacks variables.

        Parameters
        ----------
        config_settings : dict
            Path to src_dir and dest_dir as dict object, stored in config.json
        verbose : bool, optional
            Specify the verbosity of the transpiler, deafults to False

        Raises
        ------
        RuntimeError
            Raised if the config_settings point to non existing dirs.
        """

        self.src_dir = config_settings["src_dir"]
        self.dest_dir = config_settings["dest_dir"]

        if not os.path.exists(os.path.join(".", self.src_dir)):
            raise RuntimeError(
                "Source directory doesn't exist at " +
                str(self.src_dir)
            )

        if not os.path.exists(os.path.join(".", self.dest_dir)):
            raise RuntimeError(
                "Destination directory doesn't exist at " +
                str(self.dest_dir)
            )

        self.parser = "html.parser"
        self.verbose = verbose

    def __generateReactFileContent(self, soup, function_name):
        """Generates React code from HTML soup object.

        Parameters
        ----------
        soup : BeautifulSoup
            bs4.BeautifulSoup with HTML code to be transpiled.
        function_name : str
            Function name to be used from filename without extension.
        """

        # TODO: Handle function_name
        # TODO: Props and Tags

        body_contents = [
            x.encode('utf-8').decode("utf-8") for x in soup.body.contents[1:-1]
        ]
        body_str = "".join(body_contents)
        react_function = "function " + function_name + "() {return (<>" + \
            body_str + "</>);}"
        return """
        import React from 'react';
        import Helmet from 'react-helmet';

        {function}

        export default App;
        """.format(function=react_function)

    def __copyStaticFolderToDest(self):
        """Copies source static folder to the transpiled React code static
        folder inside src
        """

        static_src_dir = os.path.join(self.src_dir, "static")
        static_dest_dir = os.path.join(self.dest_dir, "src", "static")

        if not os.path.exists(static_src_dir):
            return

        if self.verbose:
            print('Copying static folder directory...')

        copy_tree(static_src_dir, static_dest_dir)

    def __transpileFile(self, filepath, is_init_html=False):
        """Transpiles the source HTML file given at the given filepath
        to a React code, which is then copied over to the React build
        directory

        Parameters
        ----------
        filepath : str
            Path to the source HTML file which is to be transpiled
        is_init_html : bool, optional
            Set to True if file to be transpiled is init html file as it will
            be renamed to App.js

        Raises
        ------
        RuntimeError
            Raised if the source html file doesn't have a .html
            extention
        """

        _, filename = os.path.split(filepath)
        filenameWithNoExtension, file_extension = os.path.splitext(filename)

        if file_extension != ".html":
            raise RuntimeError(str(filename) + ' is not a HTML file')

        if is_init_html:
            filenameWithNoExtension = "App"

        filename = filenameWithNoExtension + ".js"

        dest_filepath = os.path.join(self.dest_dir, 'src', filename)

        if self.verbose:
            print(
                "Transpiling file " + str(filepath) +
                " -> " + str(dest_filepath)
            )

        with open(filepath, 'r') as index:
            soup = BeautifulSoup(index, self.parser)

        with open(dest_filepath, 'w') as outfile:
            file_content = self.__generateReactFileContent(
                soup,
                filenameWithNoExtension
            )
            outfile.write(file_content)

    def transpile_project(self):
        """Runs initial checks like ensuring the source
        directories exist, and the source file is present.
        After that, copies static files and transpiles the source.

        Raises
        ------
        RuntimeError
            Raised source html file is missing.
        """

        entry_point_html = os.path.join(self.src_dir, 'index.html')

        if not os.path.isfile(entry_point_html):
            raise RuntimeError(
                "Entry point file doesn't exist at " +
                str(entry_point_html)
            )

        # Copy static assests
        self.__copyStaticFolderToDest()

        if self.verbose:
            print("Transpiling files...")

        # TODO: Loop through all files/dirs in src folder except
        self.__transpileFile(entry_point_html, is_init_html=True)
