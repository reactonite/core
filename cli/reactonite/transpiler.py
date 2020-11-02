import os
from bs4 import BeautifulSoup

from distutils.dir_util import copy_tree


class Transpiler:

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
        if self.verbose:
            print('Copying static folder to build directory')

        # TODO: Handle permissions issue
        copy_tree(self.src_static_dir, self.dist_static_dir)

    def __transpileFile(self, filepath):
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

    def __transpileSrc(self):
        # Copy all static assets if exists
        if(os.path.isdir(self.src_static_dir)):
            self.__copyStaticFolderToBuild()

        # TODO: Loop through all files/dirs in src folder except
        # static(NAME_STATIC_FOLDER) dir
        filepath = self.html_file_path
        self.__transpileFile(filepath)

    def transpile(self):
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

        self.__transpileSrc()
