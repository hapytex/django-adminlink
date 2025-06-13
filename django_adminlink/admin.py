from collections import defaultdict

from django.contrib import admin
from django.contrib.admin.utils import model_format_dict
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.forms import Media
from django.urls import reverse
from django.utils.html import format_html, format_html_join


class LinkFieldAdminMixin:
    admin_site_to_link = None
    admin_url_namespace = "admin"

    def _convert_list_display_item(self, field_name):
        """
        Converts a list display field name to a callable that renders a link for ForeignKey fields.

        If the specified field is a ForeignKey, returns a callable that displays the related object as a clickable link to its admin change page. Otherwise, returns the original field name.
        """
        if isinstance(field_name, str):
            try:
                field = self.model._meta.get_field(field_name)
            except FieldDoesNotExist:
                pass
            else:
                # A OneToOneField is a ForeignKey as well
                if isinstance(field, models.ForeignKey):
                    return self._link_to_model_field(field)
        return field_name

    def get_list_display(self, request):
        fields = super().get_list_display(request)
        result = []
        for field_name in fields:
            result.append(self._convert_list_display_item(field_name))
        return result

    def _link_to_model_field(self, field):
        """
        Returns a callable that renders a ForeignKey field as a clickable link to the related object's admin change page.

        If the related model is not registered with the admin site, returns the field name instead.
        """
        related_model = field.related_model
        admin_site = self.admin_site_to_link or admin.site
        model_admin = admin_site._registry.get(related_model)
        if model_admin is not None:
            url_root = f"{related_model._meta.app_label}_{related_model._meta.model_name}_change"
            if self.admin_url_namespace:
                # prefix with namespace
                url_root = f"{self.admin_url_namespace}:{url_root}"

            @admin.display(description=field.name, ordering=f"{field.name}")
            def column_render(obj):
                """
                Renders a foreign key field as a clickable link to the related object's admin change page.

                Args:
                    obj: The model instance containing the foreign key field.

                Returns:
                    An HTML anchor element linking to the related object's admin page, or None if the field is not set.
                """
                key = getattr(obj, field.name)
                if key is not None:
                    return format_html(
                        '<a title="{}" href="{}">{}</a>',
                        key,
                        reverse(url_root, kwargs={"object_id": key.pk}),
                        key,
                    )

            return column_render
        else:
            # use the field name instead, so use the old way
            return field.name


class LinkFieldAdmin(LinkFieldAdminMixin, admin.ModelAdmin):
    pass


class SingleItemActionMixin:
    action_buttons = []

    @admin.display(description="actions")
    def action_button_column(self, obj):
        """
        Renders action buttons for each object in the admin list display.

        Each button is configured with data attributes for the action name and object primary key,
        and triggers the `get_checkboxes` JavaScript function when clicked.
        """
        if isinstance(self.action_buttons, dict):
            action_buttons = self.action_buttons.items()
        else:
            action_buttons = [(x, x) for x in self.action_buttons]
        return format_html_join(
            "",
            '<button type="button" class="button button-action-{}" data-action="{}" data-pk="{}" onclick="get_checkboxes(this)">{}</button>',
            [(item, item, str(obj.pk), label) for label, item in action_buttons],
        )

    def get_list_display(self, request):
        """
        Extends the list display to include a column of action buttons if any are defined.

        If the `action_buttons` attribute is set, appends the `action_button_column` to the list
        display; otherwise, returns the default list display.
        """
        items = super().get_list_display(request)
        if self.action_buttons:
            return [*items, self.action_button_column]
        else:
            # if no action buttons are used, we can simply drop the column
            return items

    @property
    def media(self):
        """
        Extends the admin media to include JavaScript for single-item action buttons.

        Returns:
            The combined media object with the additional JavaScript file included.
        """
        return super().media + Media(js=["js/single_admin_action.js"])


class SingleItemActionAdmin(SingleItemActionMixin, admin.ModelAdmin):
    pass


def grouped_action(
    function=None, *, permissions=None, description=None, action_group=None
):
    if function is None:
        base_decorator = admin.action(permissions=permissions, description=description)

        def decorator(func):
            func = base_decorator(func)
            func.action_group = action_group
            return func

        return decorator
    else:
        function = admin.action(function)
        function.action_group = action_group
        return function


class GroupedActionAdminMixin:
    def get_action_choices(self, request, default_choices=models.BLANK_CHOICE_DASH):
        grouped_items = defaultdict(list)
        grouped_items[None].extend(default_choices)
        for func, name, description in self.get_actions(request).values():
            group = getattr(func, "action_group", None)
            choice = (name, description % model_format_dict(self.opts))
            grouped_items[group].append(choice)
        return [(k, v) for k, v in grouped_items.items()]


class GroupedActionAdmin(SingleItemActionMixin, admin.ModelAdmin):
    pass
