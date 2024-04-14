import json
import logging
from datetime import datetime
from typing import List

from main.celery import app

from .models import Statistics, Corporations


logger = logging.getLogger(__name__)


@app.task
def update_statistics(statistics_types_to_update: List[Statistics.StatisticType] = None):
    """
    Update statistics.
    :param statistics_types_to_update: List of statistics types to update. If None, all statistics will be updated.
    :return: None
    """

    logger.info("Updating statistics.")
    if statistics_types_to_update is None:
        statistics_types_to_update = list(Statistics.StatisticType)

    # Update corporation count.
    if Statistics.StatisticType.CORPORATION_COUNT in statistics_types_to_update:
        logger.debug("Updating corporation count.")
        corporation_count = Corporations.objects.count()
        Statistics.objects.update_or_create(
            type=Statistics.StatisticType.CORPORATION_COUNT,
            defaults={"value": corporation_count},
        )
        logger.debug(f"Corporation count updated: {corporation_count}.")

    # Update prefecture count.
    if Statistics.StatisticType.PREFECTURE_COUNT in statistics_types_to_update:
        logger.debug("Updating prefecture count.")
        prefecture_count = Corporations.objects.values("prefecture").distinct().count()
        Statistics.objects.update_or_create(
            type=Statistics.StatisticType.PREFECTURE_COUNT,
            defaults={"value": prefecture_count},
        )
        logger.debug(f"Prefecture count updated: {prefecture_count}.")

    # Update last update.
    if Statistics.StatisticType.LAST_UPDATE in statistics_types_to_update:
        logger.debug("Updating last update.")
        last_update = Corporations.objects.latest("updated_at").change_date
        Statistics.objects.update_or_create(
            type=Statistics.StatisticType.LAST_UPDATE,
            defaults={"value": last_update.isoformat()},
        )
        logger.debug(f"Last update updated: {last_update}.")

    # Update last updated corporations count.
    if Statistics.StatisticType.LAST_UPDATED_CORPORATIONS_COUNT in statistics_types_to_update:
        logger.debug("Updating last updated corporations count.")
        last_updated_corporations_count = Corporations.objects.filter(change_date=last_update).count()
        Statistics.objects.update_or_create(
            type=Statistics.StatisticType.LAST_UPDATED_CORPORATIONS_COUNT,
            defaults={"value": last_updated_corporations_count},
        )
        logger.debug(f"Last updated corporations count updated: {last_updated_corporations_count}.")

    logger.info("Statistics updated.")
