# Django-adminlink

[![PyPi version](https://badgen.net/pypi/v/django-adminlink/)](https://pypi.python.org/pypi/django-adminlink/)
[![Documentation Status](https://readthedocs.org/projects/django-adminlink/badge/?version=latest)](http://django-adminlink.readthedocs.io/?badge=latest)
[![PyPi license](https://badgen.net/pypi/license/django-adminlink/)](https://pypi.python.org/pypi/django-adminlink/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The Django admin allows to list rows in an easy way. Some feature that seems to be "missing" is to jump in an efficient way to the detail view of a *related* object. For example if a model `A` has a `ForeignKey` to `B`, then the `ModelAdmin` of `A` can show the `__str__` of `B`, but without a link.

This package provides a mixin to effectively add such links.

## Installation

You can install the package with:

```
pip install django-adminlink
```

## Usage

Once the package is installed, you can use the `LinkFieldAdminMixin` mixin in the admins where you want `ForeignKey`s and `OneToOneField`s to be linked to the corresponding admin detail view of that object:

```python3
from django.contrib import admin
from django_adminlink.admin import LinkFieldAdminMixin


@admin.register(Movie)
class MovieAdmin(LinkFieldAdminMixin, admin.ModelAdmin):
    list_display = ['__str__', 'genre']
```

If `genre` is a `ForeignKey` to a `Genre` model for example, and `Genre` has its own `ModelAdmin`, it will automatically convert `genre` into a column that adds a link to the admin detail view of the corresponding genre.
