# Django-adminlink

[![PyPi version](https://badgen.net/pypi/v/django-adminlink/)](https://pypi.python.org/pypi/django-adminlink/)
[![Documentation Status](https://readthedocs.org/projects/django-adminlink/badge/?version=latest)](http://django-adminlink.readthedocs.io/?badge=latest)
[![PyPi license](https://badgen.net/pypi/license/django-adminlink/)](https://pypi.python.org/pypi/django-adminlink/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The Django admin allows to list rows in an easy way. Some feature that seems to be "missing" is to jump in an efficient way to the detail view of a *related* object. For example if a model `A` has a `ForeignKey` to `B`, then the `ModelAdmin` of `A` can show the `__str__` of `B`, but without a link.

Django's admin actions are also very useful, but what seems to be missing is an easy way to just run the action on a single row without too much "hassle".

This package provides a mixin to effectively add such links.

## Installation

You can install the package with:

```
pip install django-adminlink
```

## Usage

Once the package is installed, we can work with the mixins provided by the package.

### Adding links to `ForeignKey` fields

you can use the `LinkFieldAdminMixin` mixin in the admins where you want `ForeignKey`s and `OneToOneField`s to be linked to the corresponding admin detail view of that object:

```python3
from django.contrib import admin
from django_adminlink.admin import LinkFieldAdminMixin


@admin.register(Movie)
class MovieAdmin(LinkFieldAdminMixin, admin.ModelAdmin):
    list_display = ['__str__', 'genre']
```

If `genre` is a `ForeignKey` to a `Genre` model for example, and `Genre` has its own `ModelAdmin`, it will automatically convert `genre` into a column that adds a link to the admin detail view of the corresponding genre.

### Single row actions

The package also provides a `SingleItemActionMixin`, this enables to add a column at the right end of the admin that contains (one or more) buttons. These buttons then run a Django admin action on a *single* record.

One can specify which actions to run by listing these, for example:

```python3
from django.contrib import admin
from django_adminlink.admin import SingleItemActionMixin

@admin.register(Movie)
class MovieAdmin(SingleItemActionMixin, admin.ModelAdmin):
    action_buttons = {'delete': 'delete_selected'}
```

One can work with a dictionary that has as key the "label" of the button, and as value the name (key) of the action to work with. This will add a button with the label "delete" as last column. When clicked, that row, and only that row is then removed.

The package does not perform the action itself: it works with a small amount of *JavaScript* that just disables all checkboxes, enables the one of the selected row, and finally submits the action form, and lets Django handle the logic further.

If the label(s) and action(s) are the same, one can also work with a list of the names of the actions, like:

```python3
from django.contrib import admin
from django_adminlink.admin import SingleItemActionMixin

@admin.register(Movie)
class MovieAdmin(SingleItemActionMixin, admin.ModelAdmin):
    action_buttons = ['delete_selected']
```