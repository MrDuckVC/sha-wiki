from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import View

from .forms import SearchForm, PrefectureForm
from .models import Corporations, DynamicHTMLCode


# Mixin for getting dynamic html code from database.
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


class HomeView(View, DynamicHtmlMixin):
    dynamic_html_types = [
        DynamicHTMLCode.HTMLCodeType.UPPER_RUNNING_TITLE_FOR_HOME_PAGE,
        DynamicHTMLCode.HTMLCodeType.LOWER_RUNNING_TITLE_FOR_HOME_PAGE,
    ]

    def get(self, request):
        search_form = SearchForm(data=request.GET)

        corporations = Corporations.objects.all()
        if search_form.is_valid():
            if search_form.cleaned_data["search_field"]:
                corporations = corporations.filter(
                    Q(number=search_form.cleaned_data["search_field"]) |
                    Q(name__contains=search_form.cleaned_data["search_field"]) |
                    Q(en_name__contains=search_form.cleaned_data["search_field"]) |
                    Q(prefecture__name__contains=search_form.cleaned_data["search_field"]) |
                    Q(city__name__contains=search_form.cleaned_data["search_field"]) |
                    Q(street_number__contains=search_form.cleaned_data["search_field"]) |
                    Q(post_code__contains=search_form.cleaned_data["search_field"])
                )

        page = request.GET.get("page", 1)
        paginator = Paginator(corporations, request.GET.get("page_size", 10))
        page_obj = paginator.get_page(page)

        return render(
            request,
            template_name="search_engine/corporations_list.html",
            context=self.get_context_data(
                search_form=search_form,
                page_obj=page_obj,
            ),
        )


class CorporationView(View):
    def get(self, request, corporation_number):
        corporation = get_object_or_404(Corporations, number=corporation_number)

        return render(
            request,
            template_name="search_engine/corporation.html",
            context={
                "corporation": corporation,
            },
        )


class FavoriteCorporationView(View):
    def get(self, request):
        # Get user`s favorite corporations from cookies (NOT SESSION).
        favorite_corporations = [int(corporation) for corporation in self.request.COOKIES.get("favoriteCorps", "").split(",") if corporation != ""]
        corporations = Corporations.objects.filter(number__in=favorite_corporations)

        page = request.GET.get("page", 1)
        paginator = Paginator(corporations, 20)
        page_obj = paginator.get_page(page)

        return render(
            request,
            template_name="search_engine/corporations_list.html",
            context={
                "page_obj": page_obj,
            },
        )


# Is not used yet, maybe in the future.
class PrefectureSearchView(View):
    def get(self, request):
        search_form = PrefectureForm(data=request.GET)
        corporations = Corporations.objects.all()
        if search_form.is_valid() and search_form.cleaned_data["prefecture"]:
            corporations = corporations.filter(prefecture__code__in=search_form.cleaned_data["prefecture"])

        # Pagination.
        page = request.GET.get("page", 1)
        paginator = Paginator(corporations, 20)
        page_obj = paginator.get_page(page)

        return render(
            request,
            template_name="search_engine/corporations_list_by_prefecture.html",
            context={
                "search_form": search_form,
                "page_obj": page_obj,
            },
        )
