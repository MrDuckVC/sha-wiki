from django.contrib import admin

from .models import DynamicHTMLCode


class DynamicHTMLCodeAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "enabled", "expires_at", "created_at", "updated_at")


admin.site.register(DynamicHTMLCode, DynamicHTMLCodeAdmin)
