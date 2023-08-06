=====
bjorn
=====


.. image:: https://img.shields.io/pypi/v/bjorn.svg
        :target: https://pypi.python.org/pypi/bjorn

.. image:: https://img.shields.io/travis/juanmcristobal/bjorn.svg
        :target: https://travis-ci.com/juanmcristobal/bjorn

.. image:: https://readthedocs.org/projects/bjorn/badge/?version=latest
        :target: https://bjorn.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/juanmcristobal/bjorn/shield.svg
     :target: https://pyup.io/repos/github/juanmcristobal/bjorn/
     :alt: Updates



The Bjorn module loads a configuration file for your python script.

Installation
------------

To install bjorn, run this command in your terminal:

.. code-block:: console

    $ pip install bjorn



The basics
----------
A settings file is just a Python module with module-level variables.
Settings example:

.. code-block:: python

    import os

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
            },
            "file_handler": {
                "level": "INFO",
                "filename": "/tmp/mylogfile.log",
                "class": "logging.FileHandler",
                "formatter": "standard",
            },
        },
        "loggers": {
            "job": {
                "handlers": ["default"],
                "level": os.environ.get("LOGGER_LEVEL", "INFO"),
                "propagate": True,
            },
        },
    }

    VALUE_TO_TEST = "A"

Because a settings file is a Python module, the following apply:

* It doesn’t allow for Python syntax errors.

* It can assign settings dynamically using normal Python syntax. For example:

.. code-block:: python

    MY_SETTING = [str(i) for i in range(30)]


Designating the settings
------------------------

JOB_SETTINGS
When you use Bjorn, you have to tell it which settings you’re using. Do this by using an environment variable, JOB_SETTINGS.

The value of JOB_SETTINGS should be in Python path syntax, e.g. mysite.settings. Note that the settings module should be on the Python import search path.

Usage
--------------
Create a settings.py file in the root of the project. Then you can call it from your script using the following way.

.. code-block:: python

    from bjorn.config import settings

    if __name__ == '__main__':
        print(settings.VALUE_TO_TEST)
