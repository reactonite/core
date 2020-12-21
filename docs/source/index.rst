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
-  Hot Reloading
-  Support custom scss, js, css etc.


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

0. Install the package using pip

.. code:: sh

    $ pip install reactonite

1. You are good to go, yes it's that simple... 🎉


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

    Entry point for Reactonite cli.

    Options:
    --version  Show the version and exit.
    --help     Show this message and exit.

    Commands:
    build              Command to get a static build of your app after...
    create-project     Command for creating new Reactonite project from...
    start              Command to start realtime development transpiler for...
    transpile-project  Command for transpiling a Reactonite project built...


``reactonite create-project PROJECT_NAME``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creates a Reactonite project with required directory structure. Change ``PROJECT_NAME`` to your app name.

.. code:: sh

    $ reactonite create-project my-new-project


``reactonite start``
~~~~~~~~~~~~~~~~~~~~

Starts watching for changes in Reactonite project ``src`` directory and builds the same in realtime. Requires config.json to be configured properly.

.. code:: sh

    $ reactonite start


``reactonite build``
~~~~~~~~~~~~~~~~~~~~

Generates a static build of your transpiled React app to be deployed to server. Requires config.json to be configured properly.

.. code:: sh

    $ reactonite build


``reactonite transpile-project``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Transpiles a Reactonite project created using create-project commandline. Requires ``config.json`` to be configured properly.

Available options:

* ``--verbsose`` or ``-v`` (bool): Verbosity of the command

.. code:: sh

    # verbose false by default
    $ reactonite  transpile-project
    # or with verbose
    $ reactonite  transpile-project -v


.. toctree::
   :maxdepth: 4
   :caption: Contents:

   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
