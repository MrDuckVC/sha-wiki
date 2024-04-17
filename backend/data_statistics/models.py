from django.db import models


class Statistics(models.Model):
    class StatisticType(models.TextChoices):
        CORPORATION_COUNT = "corporation_count", "Corporation count"
        PREFECTURE_COUNT = "prefecture_count", "Prefecture count"
        LAST_UPDATE = "last_update", "Last update"
        LAST_UPDATED_CORPORATIONS_COUNT = "last_updated_corporations_count", "Last updated corporations count"
        YOUNGEST_CORPORATIONS = "youngest_corporations", "Youngest corporations"
        OLDEST_CORPORATIONS = "oldest_corporations", "Oldest corporations"
        LONGEST_NAME_CORPORATIONS = "longest_name_corporations", "Longest name corporations"
        FOREIGN_CORPORATIONS = "foreign_corporations", "Foreign corporations"

    type = models.CharField(max_length=50, choices=StatisticType.choices, unique=True)
    value = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "statistics"
        verbose_name_plural = "statistics"

