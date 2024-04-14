from django.contrib import admin

from .models import DynamicHTMLCode, Statistics
from .tasks import update_statistics


def update_statistics_action(modeladmin, request, queryset):
    update_statistics.delay([stat.type for stat in queryset])


class DynamicHTMLCodeAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "enabled", "expires_at", "created_at", "updated_at")


class StatisticsAdmin(admin.ModelAdmin):
    list_display = ("type", "short_value", "created_at", "updated_at")

    def short_value(self, obj: Statistics) -> str:
        """
        Get short value.
        :param obj: Statistics object.
        :return: Short value.
        """
        if len(str(obj.value)) <= 50:
            return str(obj.value)
        return str(obj.value)[:50] + "..."

    short_value.short_description = "Value"

    actions = [update_statistics_action]


admin.site.register(DynamicHTMLCode, DynamicHTMLCodeAdmin)
admin.site.register(Statistics, StatisticsAdmin)
