import os.path
import shutil
from bs4 import BeautifulSoup
from core.config import DEFAULTS

SRC_STATIC_DIR_PATH = os.path.join(DEFAULTS.SRC_DIR, DEFAULTS.STATIC_DIR)
SRC_ENTRY_POINT_PATH = os.path.join(DEFAULTS.SRC_DIR, DEFAULTS.ENTRY_POINT_FILE)
DEST_STATIC_DIR_PATH = os.path.join(DEFAULTS.DEST_DIR, DEFAULTS.STATIC_DIR)

class Reactonite:

    def __init__(self):
        pass

    def __cleanBuildFolderIfExists(self, verbose=True):
        if(os.path.isdir(DEST_STATIC_DIR_PATH)):
            if verbose:
                print('Build folder exists at', DEST_STATIC_DIR_PATH, '. cleaning!')
            for root, dirs, files in os.walk(DEST_STATIC_DIR_PATH):
                for innerDir in dirs:
                    shutil.rmtree(os.path.join(root, innerDir))
                for innerFile in files:
                    os.remove(os.path.join(root, innerFile))
        else:
            os.mkdir(DEST_STATIC_DIR_PATH)

    def __copyStaticFolderToBuild(self, verbose=True):
        if verbose:
            print('Copying static folder to build directory')
        # TODO: Handle permissions issue
        shutil.copytree(SRC_STATIC_DIR_PATH, DEST_STATIC_DIR_PATH)

    def __transpileFile(self, filepath, verbose=True):
        _, filename = os.path.split(filepath)
        filenameWithNoExtension, file_extension = os.path.splitext(filename)

        if file_extension != ".html":
            raise Exception(filename, 'is not a HTML file')

        if verbose:
            print("Transpiling file: " + filename)
    
        with open(filepath, 'r') as index:
            soup = BeautifulSoup(index, DEFAULTS.BS_PARSER)

        with open(os.path.join(DEFAULTS.DEST_DIR, filenameWithNoExtension + ".js"), 'w') as outfile:
            function = "function App() {return (<>" + soup.html.prettify() + "</>);}"
            outfile.write(
                """
                import React from 'react';
                
                {function}
                
                export default App;
                """.format(function=function)
            )
        
    def __transpileSrc(self, verbose=True):
        # create build folder dir
        self.__cleanBuildFolderIfExists(verbose)
        
        # Copy all static assets if exists 
        if(os.path.isdir(DEFAULTS.STATIC_DIR)):
            if verbose:
                print("Coping static files")
            self.__copyStaticFolderToBuild(verbose)
        
        # Transpile all files
        if verbose:
            print("Transpiling files")

        # TODO: Loop through all files/dirs in src folder except static(NAME_STATIC_FOLDER) dir
        filepath = SRC_ENTRY_POINT_PATH
        self.__transpileFile(filepath, verbose)

    def transpile(self, verbose=False):
        # Check if entry point folder exists
        if(os.path.isdir(DEFAULTS.SRC_DIR)):
            # Check if entry point file exists
            if(os.path.isfile(SRC_ENTRY_POINT_PATH)):
                # Initial checks are done run code
                self.__transpileSrc(verbose=verbose)
            else:
                raise Exception("Entry point file doesn't exist at ", SRC_ENTRY_POINT_PATH)
        else:
            raise Exception("Entry point folder doesn't exist at ", DEFAULTS.SRC_DIR)

if __name__ == "__main__":
    reactonite = Reactonite()
    reactonite.transpile(verbose=True)
