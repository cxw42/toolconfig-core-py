# Contributing to toolconfig-core-py

Thank you!!

## Basics

* `pytest` for testing
* `black` for pretty-printing
* Python's `build` module and `setuptools` for building

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

[editable install]: https://setuptools.pypa.io/en/latest/userguide/development_mode.html
