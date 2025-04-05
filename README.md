# Django-adminlink

[![PyPi version](https://badgen.net/pypi/v/django-adminlink/)](https://pypi.python.org/pypi/django-adminlink/)
[![Documentation Status](https://readthedocs.org/projects/django-adminlink/badge/?version=latest)](http://django-adminlink.readthedocs.io/?badge=latest)
[![PyPi license](https://badgen.net/pypi/license/django-adminlink/)](https://pypi.python.org/pypi/django-adminlink/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The Django admin allows to list rows in an easy way. Some feature that seems to be "missing" is to jump in an efficient way to the detail view of a *related* object. For example if a model `A` has a `ForeignKey` to `B`, then the `ModelAdmin` of `A` can show the `__str__` of `B`, but without a link.

This package provides a mixin to effectively add such links.
