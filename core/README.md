# Reactonite Core Transpiler

Transpiler to convert HTML to React

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
