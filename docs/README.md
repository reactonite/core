<p align="center">
   <img src="https://user-images.githubusercontent.com/32339251/95760847-2265f880-0cc9-11eb-8cd5-ca641cea0771.png" alt="" width="160" />
   <h3 align="center">Reactonite's Documentation</h3>
   <p align="center">
      To generate docs for Reactonite follow these steps ✨
   </p>
</p>

## About The Project

Reactonite is a free and open source wrapper for react which lets a person write vanilla html code and convert it to a react code easily, hence building a PWA, SPA.

### Built With

This project gets documented using [Sphinx](https://www.sphinx-doc.org/en/master/) and [ReadTheDocs](https://github.com/readthedocs/sphinx_rtd_theme) specs.

## Generate Docs

Clone the repo on your local machine follow these simple steps.

### Prerequisites

Here's a list of things you'll need to have prior to documenting the software.

- Python
- NPM
- NodeJs
- Any modern web browser

### Package Installation

1. Setup virtual environment?

```sh
$ virtualenv venv
```

> Not necessary but recommended to keep your environment clean.
> Dont forget to activate it.

2. Clone the repository to local machine

```sh
$ git clone https://github.com/SDOS2020/Team_3_Reactonite.git
```

2. Install the package either using pip or python setup tools

```sh
# inside the repo root
$ pip install .
```

3. Now you have a copy of Reactonite, let's document it...

### Documentation Steps

> Note: In the same environment as previous one, follow these steps below:

1. Install documentation packages

```sh
$ cd docs/
$ pip install -r requirements.txt
```

2. Update release version if needed inside `source/conf.py`

```python
# The full version, including alpha/beta/rc tags
release = '0.0.1'
```

3. Generate `.rst` files if there are any new updates in docs

```sh
# inside docs folder still
$ sphinx-apidoc -f -o source ../reactonite
```

4. Generate html pages using `.rst` files

```sh
$ make html
# or for linux shell
$ start make.bat html
```

5. Awesome! You just documented the Reactonite Package to `build/html` 🎉

## Reference

In case you get stuck follow this link - [https://medium.com/better-programming/auto-documenting-a-python-project-using-sphinx-8878f9ddc6e9](https://medium.com/better-programming/auto-documenting-a-python-project-using-sphinx-8878f9ddc6e9) which offers a detailed guide on the same.
