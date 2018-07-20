.. image:: https://img.shields.io/travis/macisamuele/language-formatters-pre-commit-hooks.svg
  :target: https://travis-ci.org/macisamuele/language-formatters-pre-commit-hooks?branch=master

.. image:: https://img.shields.io/codecov/c/github/macisamuele/language-formatters-pre-commit-hooks/master.svg
  :target: https://codecov.io/gh/macisamuele/language-formatters-pre-commit-hooks

.. image:: https://img.shields.io/pypi/v/language-formatters-pre-commit-hooks.svg
    :target: https://pypi.python.org/pypi/language-formatters-pre-commit-hooks/
    :alt: PyPi version

.. image:: https://img.shields.io/pypi/pyversions/language-formatters-pre-commit-hooks.svg
    :target: https://pypi.python.org/pypi/language-formatters-pre-commit-hooks/
    :alt: Supported Python versions

Language Formatters Pre Commit Hooks
====================================

About
-----

This package provides utilities for ensuring that your code is nicely formatted by using `pre-commit <https://pre-commit.com/>`__ hooks

Example Usage
-------------

Add a similar snippet into your ``.pre-commit-config.yaml`` file

.. code-block:: yaml

    - repo: git@github.com:macisamuele/language-formatters-pre-commit-hooks
      rev: ${LATEST_SHA}
      hooks:
      - id: pretty-format-java
        args: [--autofix]
      - id: pretty-format-kotlin
        args: [--autofix]
      - id: pretty-format-yaml
        args: [--autofix, --indent, '2']


Development
===========

This tool uses tox as main tool to build virtual environments.
To get started will be enough to run ``make development``

If you have `aactivator <https://github.com/Yelp/aactivator>`_ installed this step will happen automatically.

Contributing
------------

1. Fork it ( http://github.com/macisamuele/language_formatters_pre_commit_hooks/fork )
2. Create your feature branch (``git checkout -b my-new-feature``)
3. Add your modifications
4. Push to the branch (``git push origin my-new-feature``)
5. Create new Pull Request

License
-------

``language-formatters-pre-commit-hooks`` is licensed with a `Apache License version 2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>`__.
