import os
from distutils.dir_util import copy_tree

from bs4 import BeautifulSoup


class Transpiler:
    """Transpiler responsible for translating HTML code to React

    Attributes
    ----------
    src_dir : str
        Path of the source directory within the project directory
    html_file_path : str
        Path of the source HTML file within the source directory
    src_static_dir : str
        Path of the source static directory containing static files
    dist_dir : str
        Path to the transpiled React app within the project directory
    dist_src_dir : str
        Path to the source directory of the transpiled React app
    dist_static_dir : str
        Path to the static directory used by the transpiled React app
    parser : str, optional
        Default value : "html.parser"
        Specify which parser to use for reading HTML files
    verbose : bool, optional
        Default value : False
        Specify the verbosity of the transpiler

    Methods
    -------
    __copyStaticFolderToBuild()
        Copies source static folder to the transpiled React app
    __transpileFile(filepath)
        Translates the given file to React code
    transpile()
        Runs checks and calls __copyStaticFolderToBuild and
        __transpileFile

    """
    def __init__(self,
                 src_dir,
                 html_file_path,
                 src_static_dir,
                 dist_dir,
                 dist_src_dir,
                 dist_static_dir,
                 parser="html.parser",
                 verbose=False):

        self.src_dir = src_dir
        self.html_file_path = html_file_path
        self.src_static_dir = src_static_dir
        self.dist_dir = dist_dir
        self.dist_src_dir = dist_src_dir
        self.dist_static_dir = dist_static_dir
        self.parser = parser
        self.verbose = verbose

    def __copyStaticFolderToBuild(self):
        """Copies source static folder to the transpiled React code
        """

        if self.verbose:
            print('Copying static folder to build directory')

        # TODO: Handle permissions issue
        copy_tree(self.src_static_dir, self.dist_static_dir)

    def __transpileFile(self, filepath):
        """Transpiles the source HTML file given at the given filepath
        to a React code, which is then copied over to the React build
        directory

        Parameters
        ----------
        filepath : str
            Path to the source HTML file which is to be transpiled
        """

        _, filename = os.path.split(filepath)
        filenameWithNoExtension, file_extension = os.path.splitext(filename)
        filename = filenameWithNoExtension + ".js"

        if file_extension != ".html":
            raise Exception(filename, 'is not a HTML file')

        if self.verbose:
            print("Transpiling file: " + filename)

        with open(filepath, 'r') as index:
            soup = BeautifulSoup(index, self.parser)

        with open(os.path.join(self.dist_src_dir, filename),
                  'w') as outfile:
            function = "function App() {return (<>" + \
                        soup.html.prettify() + \
                        "</>);}"
            outfile.write(
                """
import React from 'react';

{function}

export default App;
                """.format(function=function)
            )

    def transpile(self):
        """Runs initial checks like ensuring the source
        directories exist, and the source file is present.
        After that, call __copyStaticFolderToBuild() and
        __transpileFile methods to transpile the source.
        """

        # Check if entry point folder exists
        if os.path.isdir(self.src_dir):
            # Check if entry point file exists
            if os.path.isfile(self.html_file_path):
                # Initial checks are done run code
                pass
            else:
                raise Exception("Entry point file doesn't exist at",
                                self.html_file_path)
        else:
            raise Exception("Entry point folder doesn't exist at",
                            self.src_dir)

        # Copy all static assets if exists
        if(os.path.isdir(self.src_static_dir)):
            self.__copyStaticFolderToBuild()

        # TODO: Loop through all files/dirs in src folder except
        # static(NAME_STATIC_FOLDER) dir
        filepath = self.html_file_path
        self.__transpileFile(filepath)
