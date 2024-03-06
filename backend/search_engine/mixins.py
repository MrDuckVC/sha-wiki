from django.db.models import Q
from django.utils import timezone

from .models import DynamicHTMLCode


class DynamicHtmlMixin:
    """
    Mixin for getting dynamic html code from database.
    It will be transferred to the template as a context variable.
    """

    # Types of html code that can be transferred to the template.
    dynamic_html_types: list[DynamicHTMLCode.HTMLCodeType] = []

    def get_context_data(self, **kwargs):
        context = kwargs

        context["dynamic_html"] = {}
        for html_type in self.dynamic_html_types:
            html_codes = DynamicHTMLCode.objects.filter(
                Q(type=html_type) &
                Q(enabled=True) & (
                    Q(expires_at__isnull=True) |
                    Q(expires_at__gte=timezone.now())
                )
            ).all()
            if html_codes:
                context["dynamic_html"][html_type] = html_codes
        return context
