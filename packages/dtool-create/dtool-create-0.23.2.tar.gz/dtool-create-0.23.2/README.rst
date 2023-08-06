dtool CLI commands for creating datasets
========================================

.. image:: https://badge.fury.io/py/dtool-create.svg
   :target: http://badge.fury.io/py/dtool-create
   :alt: PyPi package

.. image:: https://travis-ci.org/jic-dtool/dtool-create.svg?branch=master
   :target: https://travis-ci.org/jic-dtool/dtool-create
   :alt: Travis CI build status (Linux)

.. image:: https://ci.appveyor.com/api/projects/status/3300cl94ajot1231/branch/master?svg=true
   :target: https://ci.appveyor.com/project/tjelvar-olsson/dtoolcore
   :alt: AppVeyor CI build status (Windows)

.. image:: https://codecov.io/github/jic-dtool/dtool-create/coverage.svg?branch=master
   :target: https://codecov.io/github/jic-dtool/dtool-create?branch=master
   :alt: Code Coverage


Installation
------------

.. code-block:: bash

    pip install dtool-create

.. warning:: In order to be able to install the ``ryamel.yaml``
             dependency you may need to run::

                pip install -U pip setuptools wheel

             See http://yaml.readthedocs.io/en/latest/install.html
             for more details.


Usage
-----

Create a proto dataset::

    dtool create my_dataset

Add some data to to the dataset::

    cp *.csv my_dataset/data

Add descriptive metadata to the dataset::

    dtool readme interative my_dataset

Convert the proto dataset to a dataset by freezing it::

    dtool freeze my_dataset

See the `dtool documentation <http://dtool.readthedocs.io>`_ for more detail.


Configuring the descriptive metadata template
---------------------------------------------

It is possible to configure the required metadata prompted for by the
``dtool readme interactive`` command. The default template is the
``dtool_create/templates/README.yml``.

One may want to create a custom YAML file specifying the required metadata
that will be prompted for. This can be achieved by setting the
``DTOOL_README_TEMPLATE_FPATH`` environment variable, e.g.::

    export DTOOL_README_TEMPLATE_FPATH=~/dtool_readme.yml

Alternatively, one can add the ``DTOOL_README_TEMPLATE_FPATH`` key to the
``~/.config/dtool/dtool.json`` file.  For example,

.. code-block:: json

    {
       "DTOOL_README_TEMPLATE_FPATH": "/Users/olssont/dtool_readme.yml"
    }

If the ``~/.config/dtool/dtool.json`` file does not exist one may need to
create it.


Configuring the user's full name and email for the descriptive metadata
-----------------------------------------------------------------------

When running the ``dtool interactive readme`` the default name and email
address are ``Your Name`` and ``you@example.com``.  These defaults can be
configured by setting the ``DTOOL_USER_FULL_NAME`` ``DTOOL_USER_EMAIL``
environment variables.

::

    export DTOOL_USER_FULL_NAME="Care A. Bout-Data"
    export DTOOL_USER_EMAIL=researcher@famous.uni.ac.uk

Alternatively, one can add the ``DTOOL_USER_FULL_NAME`` and
``DTOOL_USER_EMAIL`` keys to the ``~/.config/dtool/dtool.json`` file.  For
example,

.. code-block:: json

    {
       "DTOOL_USER_FULL_NAME": "Care A. Bout-Data",
       "DTOOL_USER_EMAIL": "researcher@famous.uni.ac.uk"
    }

If the ``~/.config/dtool/dtool.json`` file does not exist one may need to
create it.


Related packages
----------------

- `dtoolcore <https://github.com/jic-dtool/dtoolcore>`_
- `dtool-cli <https://github.com/jic-dtool/dtool-cli>`_
- `dtool-config <https://github.com/jic-dtool/dtool-config>`_
- `dtool-info <https://github.com/jic-dtool/dtool-info>`_
