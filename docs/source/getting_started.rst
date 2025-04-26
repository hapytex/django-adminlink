===============
Getting started
===============

Once the package is installed, you can use the `LinkFieldAdminMixin` mixin in the admins where you want `ForeignKey`s and `OneToOneField`s to be linked to the corresponding admin detail view of that object:

  .. code-block:: python3

   from django.contrib import admin


   @admin.register(Movie)
   class MovieAdmin(LinkFieldAdminMixin, admin.ModelAdmin):
       list_display = ['__str__', 'genre']

If `genre` is a `ForeignKey` to a `Genre` model for example, and `Genre` has its own `ModelAdmin`, it will automatically convert `genre` into a column that adds a link to the admin detail view of the corresponding genre.


Another option is to use with the `SingleItemActionMixin` to add a button per row to do (one or more) actions for that specific line with:

  ..code-block:: python3

   from django.contrib import admin
   from django_adminlink.admin import SingleItemActionMixin

   @admin.register(Movie)
   class MovieAdmin(SingleItemActionMixin, admin.ModelAdmin):
       action_buttons = {'delete': 'delete_selected'}

here the `action_buttons` is a dictionary (or list) of labels that map to the admin actions. If the label is the same for each admin action, you can use a list, where you thus list the label and admin action only once.