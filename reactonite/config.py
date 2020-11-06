class DEFAULTS:
    """Default variables used in code execution

    Attributes
    ----------
    INIT_FILES_DIR : str
        Directory for initial files for setup.
    SRC_DIR : str
        Source directory for reactonite codebase.
    DEST_DIR : str
        Destination directory for React codebase.
    CONFIG_FILE_NAME : str
        Config file name for config variables.
    """

    def __init__(self):
        self.INIT_FILES_DIR = 'init_src_dir'
        self.SRC_DIR = 'src'
        self.DEST_DIR = 'dist'
        self.CONFIG_FILE_NAME = 'config.json'
