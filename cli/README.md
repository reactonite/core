# Reactonite

Transpiler to convert HTML to React

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

# Reactonite Core Transpiler

## How to setup

1. Use a virtual environment?
2. Install the required packages using pip.

   ```bash
   pip install -r requirements.txt
   ```

3. Write your code in `src` folder basic file structure is already provided.
   > Note: If not already present use `reactonite-cli` to create a react app and set corresponding path in `main.py`
4. Call `main.py` from the command line to run the transpiler.

   ```bash
   python main.py
   ```

## Current Features

- [x] Transpiles index.html files inside src folder to react app and copies static files

  ```bash
  python main.py
  ```

- [ ] Convert all \*.html
- [ ] Auto create-react-app on first install
