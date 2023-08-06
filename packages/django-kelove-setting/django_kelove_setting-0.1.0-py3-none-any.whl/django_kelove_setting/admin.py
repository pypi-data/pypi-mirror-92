"""
admin.py
By IT小强xqitw.cn <mail@xqitw.cn>
At 1/24/21 11:29 AM
"""

from collections import Iterable
from importlib import import_module

from django.contrib.admin import ModelAdmin, site
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.apps import apps

from .models import Settings as SettingsModel
from .setting_forms import Settings as SettingsForm


def load_object(path: str):
    """
    Load an object given its absolute object path, and return it.
    object can be a class, function, variable or an instance.
    path ie: 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware'
    """

    dot = path.rindex('.')
    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)
    return getattr(mod, name)


class SettingsModelAdmin(ModelAdmin):
    """
    配置管理
    """

    change_form_template = 'kelove_setting/change_form.html'

    list_display = (
        'id',
        'settings_title',
        'settings_key',
        'created_user',
        'created_time',
        'updated_user',
        'updated_time',
    )

    list_display_links = ('settings_title', 'settings_key')

    list_filter = ('created_time', 'updated_time')

    search_fields = ('settings_title', 'settings_key')

    readonly_fields = ('settings_title', 'settings_key')

    def get_fieldsets(self, request, obj=None):
        """
        Hook for specifying fieldsets.
        :param request:
        :param obj:
        :return:
        """
        form = self.get_form(request=request, obj=obj)
        if form.fieldsets:
            return form.fieldsets
        fieldsets = form.get_fieldsets(model_admin=self, request=request, obj=obj)
        if fieldsets:
            return fieldsets
        return super().get_fieldsets(request=request, obj=obj)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return super().has_change_permission(request, obj)
        return request.user.has_perm(obj.get_settings_permission_code('change'))

    def has_delete_permission(self, request, obj=None):
        if not obj:
            return super().has_delete_permission(request, obj)
        return request.user.has_perm(obj.get_settings_permission_code('delete'))

    def has_view_permission(self, request, obj=None):
        if not obj:
            return super().has_view_permission(request, obj)
        return (
                request.user.has_perm(obj.get_settings_permission_code('change')) or
                request.user.has_perm(obj.get_settings_permission_code('view'))
        )

    def add_view(self, request, form_url='', extra_context=None):
        """
        初始化
        :param request:
        :param form_url:
        :param extra_context:
        :return:
        """
        kelove_settings_app_key = 'kelove_settings'
        app_configs = apps.get_app_configs()
        kelove_settings = [
            j
            for i in app_configs
            for j in getattr(i, kelove_settings_app_key, [])
            if
            hasattr(i, kelove_settings_app_key)
            and isinstance(getattr(i, kelove_settings_app_key, []), Iterable)
            and not isinstance(getattr(i, kelove_settings_app_key, []), str)
        ]

        for form in kelove_settings:
            if isinstance(form, str):
                try:
                    form = load_object(form)
                except ModuleNotFoundError:
                    continue

            if not issubclass(form, SettingsForm):
                continue

            obj, is_create = SettingsModel.objects.get_or_create(
                settings_key=form.get_settings_key(),
                settings_title=form.get_settings_title(is_full=False),
                settings_val=form.get(),
                created_user=request.user,
                updated_user=request.user
            )
            obj.create_admin_settings_auth()
            form.delete_cache()

        opts = self.model._meta
        obj_url = reverse(
            'admin:%s_%s_changelist' % (opts.app_label, opts.model_name),
            current_app=self.admin_site.name,
        )
        return HttpResponseRedirect(obj_url)

    def get_form(self, request, obj=None, change=False, **kwargs):
        if obj:
            try:
                form = load_object(obj.settings_key)
                if issubclass(form, SettingsForm):
                    return form
            except AttributeError:
                pass
        return super().get_form(request, obj, change, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        自动写入创建用户ID和更新用户ID
        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        """

        if request.user:
            user = request.user
            obj.updated_user = user
            if not change:
                obj.created_user = user
        super().save_model(request, obj, form, change)


if not site.is_registered(SettingsModel):
    site.register(SettingsModel, SettingsModelAdmin)
