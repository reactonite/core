import os.path
import shutil
from bs4 import BeautifulSoup

PATH_INPUT_FOLDER = "src"
NAME_STATIC_FOLDER = "static"
PATH_STATIC_FOLDER = os.path.join(PATH_INPUT_FOLDER, NAME_STATIC_FOLDER)
ENTRY_POINT_FILENAME = "App.html"
ENTRY_POINT_FILE_PATH = os.path.join(PATH_INPUT_FOLDER, ENTRY_POINT_FILENAME)

PATH_OUTPUT_FOLDER = "dist/src/reactonite-code"
PATH_STATIC_FOLDER_OUTPUT = os.path.join(PATH_OUTPUT_FOLDER, NAME_STATIC_FOLDER)

class Reactonite:

    def __init__(self):
        self.PARSER = "html.parser"

    def __cleanBuildFolderIfExists(self):
        if(os.path.isdir(PATH_OUTPUT_FOLDER)):
            for root, dirs, files in os.walk(PATH_OUTPUT_FOLDER):
                for innerDir in dirs:
                    shutil.rmtree(os.path.join(root, innerDir))
                for innerFile in files:
                    os.remove(os.path.join(root, innerFile))
        else:
            os.mkdir(PATH_OUTPUT_FOLDER)

    def __copyStaticFolderToBuild(self):
        shutil.copytree(PATH_STATIC_FOLDER, PATH_STATIC_FOLDER_OUTPUT)

    def __transpileFile(self, filepath, verbose):

        _, filename = os.path.split(filepath)
        filenameWithNoExtension, file_extension = os.path.splitext(filename)

        if file_extension != ".html":
            return

        if verbose:
            print("Transpiling file: " + filename)
    
        with open(filepath, 'r') as index:
            soup = BeautifulSoup(index, 'html.parser')

        with open(os.path.join(PATH_OUTPUT_FOLDER, filenameWithNoExtension + ".js"), 'w') as outfile:
            function = "function App() {return (<>" + soup.html.prettify() + "</>);}"
            outfile.write(
                """
                import React from 'react';
                
                {function}
                
                export default App;
                """.format(function=function)
            )
        
    def __transpileSrc(self, verbose):
        # create build folder dir
        if verbose:
            print("Cleaning build folder...")
        self.__cleanBuildFolderIfExists()
        
        # Copy all static assets if exists 
        if(os.path.isdir(PATH_STATIC_FOLDER)):
            if verbose:
                print("Coping static files...")
            self.__copyStaticFolderToBuild()
        
        # Transpile all files
        if verbose:
            print("Transpiling files...")
        # TODO: Loop through all files/dirs in src folder except static(NAME_STATIC_FOLDER) dir
        filepath = os.path.join(PATH_INPUT_FOLDER, ENTRY_POINT_FILENAME)
        self.__transpileFile(filepath, verbose)

    def transpile(self, verbose=False):
        # Check if entry point folder exists
        if(os.path.isdir(PATH_INPUT_FOLDER)):
            # Check if entry point file exists
            if(os.path.isfile(ENTRY_POINT_FILE_PATH)):
                # Initial checks are done run code
                self.__transpileSrc(verbose=verbose)
            else:
                raise OSError("Entry point file doesn't exists " + ENTRY_POINT_FILE_PATH)
        else:
            raise OSError("Entry point folder doesn't exists " + PATH_INPUT_FOLDER)

if __name__ == "__main__":
    reactonite = Reactonite()
    reactonite.transpile(verbose=True)
