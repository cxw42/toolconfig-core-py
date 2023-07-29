# Contributing to toolconfig-core-py

Thank you!!

## Basics

* `pytest` for testing
* `black` for pretty-printing
* Python's `build` module and `setuptools` for building
* `sphinx` for documentation

`Makefile` gives you convenient access to common development commands.

## Workflow

Setup: `make init`

Then:

1. Write tests
2. Hack hack!
3. `make test`
4. `make prettyprint`
5. Commit

## Running the CLI

```
$ PYTHONPATH=src python -m toolconfig [ARGS]...
```
or run in an [editable install].

## Documentation

Docstrings are in [Google format].

To generate docs, say `make html` and then open `doc/build/html/index.html`.

[editable install]: https://setuptools.pypa.io/en/latest/userguide/development_mode.html
[Google format]: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
