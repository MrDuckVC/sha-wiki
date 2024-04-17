from django.shortcuts import render
from django.views import View

from .models import Statistics


class HomeView(View):
    def get(self, request):
        return render(
            request,
            template_name="data_statistics/home.html",
            context={
                "corporations_amount": Statistics.objects.filter(type=Statistics.StatisticType.CORPORATION_COUNT).first().value,
                "prefectures_amount": Statistics.objects.filter(type=Statistics.StatisticType.PREFECTURE_COUNT).first().value,
                "youngest_corps": Statistics.objects.filter(type=Statistics.StatisticType.YOUNGEST_CORPORATIONS).first().value[:10],
                "oldest_corps": Statistics.objects.filter(type=Statistics.StatisticType.OLDEST_CORPORATIONS).first().value[:10],
                "longest_names_corps": Statistics.objects.filter(type=Statistics.StatisticType.LONGEST_NAME_CORPORATIONS).first().value[:10],
                "foreign_address_corps": Statistics.objects.filter(type=Statistics.StatisticType.FOREIGN_CORPORATIONS).first().value[:10],
                "most_changes_corps": [],  # TODO: Add list of corps with most amount of updates (most_changes_corps).
            },
        )
