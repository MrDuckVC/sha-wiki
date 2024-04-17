import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View

from .forms import SearchForm, PrefectureForm
from .mixins import DynamicHtmlMixin
from .models import Corporations, DynamicHTMLCode
from data_statistics.models import Statistics


class HomeView(View, DynamicHtmlMixin):
    dynamic_html_types = [
        DynamicHTMLCode.HTMLCodeType.UPPER_RUNNING_TITLE_FOR_HOME_PAGE,
        DynamicHTMLCode.HTMLCodeType.LOWER_RUNNING_TITLE_FOR_HOME_PAGE,
    ]

    def get(self, request):
        search_form = SearchForm(data=request.GET)

        # Get statistics.
        last_update = Statistics.objects.filter(type=Statistics.StatisticType.LAST_UPDATE).first().value
        updated_corporations_count = Statistics.objects.filter(type=Statistics.StatisticType.LAST_UPDATED_CORPORATIONS_COUNT).first().value

        corporations = Corporations.objects.all()
        if search_form.is_valid() and search_form.cleaned_data["search_field"]:
            corporations = Corporations.objects.all().filter(
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
                last_update=last_update,
                updated_corporations_count=updated_corporations_count,
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
            template_name="search_engine/favorite_corporations_list.html",
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
