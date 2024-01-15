from django import template

from search_engine.models import Corporations


register = template.Library()


@register.inclusion_tag("search_engine/templatetags/corporation_card.html")
def corporation_card(corp: Corporations):
    """
    Returns a corporation card.
    """
    return {"corp": corp}
