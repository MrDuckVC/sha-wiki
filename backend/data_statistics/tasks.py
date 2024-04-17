import logging
from typing import List

from main.celery import app

from .models import Statistics
from search_engine.models import Corporations


logger = logging.getLogger(__name__)


@app.task
def update_statistics(statistics_types_to_update: List[Statistics.StatisticType] = None) -> None:
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

    def corporation_entity_to_dict(corporation: Corporations) -> dict:
        """
        Convert corporation entity to dictionary for JSON serialization.
        :param corporation: Corporation entity.
        :return: Dictionary.
        """
        return {
            "id": corporation.id,
            "number": corporation.number,
            "update_date": corporation.update_date.isoformat(),
            "change_date": corporation.change_date.isoformat(),
            "name": corporation.name,
            "street_number": corporation.street_number,
            "post_code": corporation.post_code,
            "address_outside": corporation.address_outside,
            "en_name": corporation.en_name,
            "furigana": corporation.furigana,
            "hihyoji": corporation.hihyoji,
            "prefecture": corporation.prefecture.name if corporation.prefecture else None,
            "city": corporation.city.name if corporation.city else None,
            "created_at": corporation.created_at.isoformat(),
            "updated_at": corporation.updated_at.isoformat(),
        }

    # Update youngest corporations.
    if Statistics.StatisticType.YOUNGEST_CORPORATIONS in statistics_types_to_update:
        logger.debug("Updating youngest corporations.")
        Statistics.objects.update_or_create(
            type=Statistics.StatisticType.YOUNGEST_CORPORATIONS,
            defaults={"value": [
                corporation_entity_to_dict(corporation)
                for corporation in Corporations.objects.order_by("-change_date")[:100]
            ]},
        )
        logger.debug(f"Youngest corporations updated.")

    # Update oldest corporations.
    if Statistics.StatisticType.OLDEST_CORPORATIONS in statistics_types_to_update:
        logger.debug("Updating oldest corporations.")
        Statistics.objects.update_or_create(
            type=Statistics.StatisticType.OLDEST_CORPORATIONS,
            defaults={"value": [
                corporation_entity_to_dict(corporation)
                for corporation in Corporations.objects.order_by("change_date")[:100]
            ]},
        )
        logger.debug(f"Oldest corporations updated.")

    # Update longest name corporations.
    if Statistics.StatisticType.LONGEST_NAME_CORPORATIONS in statistics_types_to_update:
        logger.debug("Updating longest name corporations.")
        Statistics.objects.update_or_create(
            type=Statistics.StatisticType.LONGEST_NAME_CORPORATIONS,
            defaults={"value": [
                corporation_entity_to_dict(corporation)
                for corporation in Corporations.objects.extra(select={"length": "Length(name)"}).order_by("-length")[:100]
            ]},
        )
        logger.debug(f"Longest name corporations updated.")

    # Update foreign corporations.
    if Statistics.StatisticType.FOREIGN_CORPORATIONS in statistics_types_to_update:
        logger.debug("Updating foreign corporations.")
        Statistics.objects.update_or_create(
            type=Statistics.StatisticType.FOREIGN_CORPORATIONS,
            defaults={"value": [
                corporation_entity_to_dict(corporation)
                for corporation in Corporations.objects.filter(address_outside__isnull=False).order_by("name")[:100]
            ]},
        )
        logger.debug(f"Foreign corporations updated.")

    logger.info("Statistics updated.")
