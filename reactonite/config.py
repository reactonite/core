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

    INIT_FILES_DIR = 'init_src_dir'
    SRC_DIR = 'src'
    DEST_DIR = 'dist'
    STATIC_DIR = 'static'
    HTML_FILE_PATH = 'index.html'
    CONFIG_FILE_PATH = 'config.json'
    BS_PARSER = 'html.parser'
