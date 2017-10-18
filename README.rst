===============================
rt_factory
===============================


.. image:: https://img.shields.io/pypi/v/rt_factory.svg
        :target: https://pypi.python.org/pypi/rt_factory

.. image:: https://img.shields.io/travis/ptillemans/rt_factory.svg
        :target: https://travis-ci.org/ptillemans/rt_factory

.. image:: https://readthedocs.org/projects/rt-factory/badge/?version=latest
        :target: https://rt-factory.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/melexis/rt_factory/shield.svg
     :target: https://pyup.io/repos/github/melexis/rt_factory/
     :alt: Updates


Pythonic wrapper for the artifactory API


* Free software: Apache Software License 2.0
* Documentation: https://rt-factory.readthedocs.io.


Features
--------

* TODO

Installation
------------

on OSX you need to have the openssl headers and libraries installed and added to
the include and library search paths in order to compile the *cryptography*
package.

.. code:: sh
  $ brew install openssl
  $ export LDFLAGS="-L/usr/local/opt/openssl/lib"
  $ export CPPFLAGS="-I/usr/local/opt/openssl/include"
  $ export PKG_CONFIG_PATH="/usr/local/opt/openssl/lib/pkgconfig"

For linux you need to install *libssl-dev* on debian based systems or *openssl-devel*
on RPM based systems.

Once these dependencies are installed, just pip install the dev requirements.

.. code:: sh
  $ pip install -r requirements_dev.txt


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

