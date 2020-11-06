.. Reactonite documentation master file, created by
   sphinx-quickstart on Fri Nov  6 17:32:22 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Reactonite's documentation!
======================================

About The Project
-----------------

Reactonite is a free and open source wrapper for react which lets a
person write vanilla html code and convert it to a react code easily,
hence building a PWA, SPA ✨

Here's the key features added to Reactonite:

-  Transpile HTML code to React website
-  Create PWAs and React applications as quickly as possible
-  Act as a wrapper to NPM
-  Allow importing of already created HTML file components
-  Hot Reloading
-  Support custom scss, styled-components, material icons etc.


Getting Started
---------------

To get this repo up and running on your local machine follow these
simple steps.

Prerequisites
-------------

Here's a list of things you'll need to have prior to installing the
software.

-  Python
-  NPM
-  NodeJs
-  Any modern web browser

Installation
------------

1. Setup virtual environment?

.. code:: sh

    $ virtualenv venv

> Not necessary but recommended to keep your environment clean.
> Dont forget to activate it.

2. Clone the repository to local machine.

.. code:: sh

    $ git clone https://github.com/SDOS2020/Team_3_Reactonite.git

3. Install the package either using pip or python setup tools

.. code:: sh

    $ python setup.py install
    # Use `develop` instead of `install` to get an editable build

    # Alternatively run
    $ pip install .

4. You are good to go... 🎉


Usage
-----

Once installed here are the commands that will allow you to create
Reactonite projects.

``reactonite --help``
~~~~~~~~~~~~~~~~~~~~~

Opens the help page for ``reactonite`` commandline.

.. code:: sh

    $ reactonite --help
    Usage: reactonite [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      create-project
      watch

``reactonite create-project PROJECT_NAME``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creates a reactonite app project with required directory structure.
Change ``PROJECT_NAME`` to your app name.

.. code:: sh

    $ reactonite create-project my-new-project


.. toctree::
   :maxdepth: 4
   :caption: Contents:

   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
