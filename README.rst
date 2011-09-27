django-extraconfig
==================

With ``django-extraconfig`` it's easy to extend a Django project
``settings.py`` file. The only function provided by this module is
``load_extraconfig(entry_point_name, module_name)``.

``extraconfig.load(entry_point_name, module_name)``
    Loads all uppercase values from the entry point modules
    into the module with the name ``module_name`` overriding
    any existing values.

Usage
=====

At the bottom of your ``settings.py`` file add::

    try:
        import extraconfig
    except ImportError:
        pass
    else:
        extraconfig.load(<entry_point_name>, __name__)

``entry_point_name`` can be any string value but it's a good practice to
include the projectname in order to avoid name collisions. For example to
load the extra configuration showed below, ``entry_point_name`` should be
set to *"my_project.extraconfig"*.

Creating an extra configuration
===============================

It's easy to create an extra configuration module. The minimal project
layout is composed of two files: ``setup.py`` and the module file. The module
will be installed using the ``setup.py`` file just like any other regular
Python module. In order for ``django-extraconfig`` to know that this module
should be used to override your Django configuration in ``setup.py`` you must
add it in the entry point config.

A minimal ``setup.py`` file can look like this::

    from setuptools import setup

    setup(
        name='my_extra_config',
        version='0.1',
        py_modules=['my_extra_config'],
        entry_points = {
            'my_project.extraconfig': 'main = my_extra_config'
        }
    )

Now you can add a ``my_extra_config.py`` file with the settings you want to
override::

    DEBUG = True

Installing the extra configuration
==================================

Once the extra configuration project is ready you can run::

    python setup.py develop

This will install the extra configuration module in development mode, meaning
you can edit the extra settings and all the changes will be visible without
reinstalling it.
