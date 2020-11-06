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
    STATIC_DIR : str
        Static folder name for assets to be copied.
    HTML_FILE_PATH : str
        Init file path to be generated for new projects.
    CONFIG_FILE_PATH : str
        Config file path for config variables.
    BS_PARSER : str
        Parser to be used for transpilation.
    """

    def __init__(self):
        self.INIT_FILES_DIR = 'init_src_dir'
        self.SRC_DIR = 'src'
        self.DEST_DIR = 'dist'
        self.STATIC_DIR = 'static'
        self.HTML_FILE_PATH = 'index.html'
        self.CONFIG_FILE_PATH = 'config.json'
        self.BS_PARSER = 'html.parser'
