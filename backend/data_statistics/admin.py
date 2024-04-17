from django.contrib import admin

from .models import Statistics
from .tasks import update_statistics


def update_statistics_action(modeladmin, request, queryset):
    update_statistics.delay([stat.type for stat in queryset])


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


admin.site.register(Statistics, StatisticsAdmin)
