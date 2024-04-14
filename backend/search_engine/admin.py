from django.contrib import admin

from .models import DynamicHTMLCode, Statistics
from .tasks import update_statistics


def update_statistics_action(modeladmin, request, queryset):
    update_statistics.delay([stat.type for stat in queryset])


class DynamicHTMLCodeAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "enabled", "expires_at", "created_at", "updated_at")


class StatisticsAdmin(admin.ModelAdmin):
    list_display = ("type", "value", "created_at", "updated_at")
    actions = [update_statistics_action]


admin.site.register(DynamicHTMLCode, DynamicHTMLCodeAdmin)
admin.site.register(Statistics, StatisticsAdmin)
