============
Installation
============

The package can be fetched as `django-adminlink`, so for example with `pip` with:

.. code-block:: console
   
   pip3 install django-adminlink

The item is a Django app, but you do not per se have to install it as such. If you don't make use of the `SingleItemActionMixin`,
you don't need to add `'django_adminlink'` to the `INSTALLED_APPS`, otherwise you need to do this to include the static file.