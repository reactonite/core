# Reactonite

From HTML to React

## How to setup

1. Use a virtual environment?
2. Install the package either using pip or python setup tools

   ```bash
   python setup.py install # Use `develop` instead of `install` to get an editable build
   or
   pip install .
   ```

3. Call `reactonite` from the command line.

   ```bash
   $ reactonite --help
   Usage: reactonite [OPTIONS] COMMAND [ARGS]...

   Options:
     --help  Show this message and exit.

   Commands:
     create-empty-project
   ```

## Current Features

- [x] Create a react app from the command line by:

  ```bash
  reactonite create-empty-project my-new-app
  ```

- [ ] Create a react app from a given HTML file.
- [ ] Specify a react app dir and an HTML file to update an existitng project.
