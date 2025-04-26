from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.forms import Media
from django.urls import reverse
from django.utils.html import format_html_join


class LinkFieldAdminMixin:
    admin_site_to_link = None
    admin_url_namespace = "admin"

    def _convert_list_display_item(self, field_name):
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
        items = super().get_list_display(request)
        if self.action_buttons:
            return [*items, self.action_button_column]
        else:
            # if no action buttons are used, we can simply drop the column
            return items

    @property
    def media(self):
        return super().media + Media(js=["js/single_admin_action.js"])
