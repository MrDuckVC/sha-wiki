from typing import Iterable
from urllib.parse import urlparse, parse_qs, urlunparse

from django import template
from django.core.paginator import Page
from django.utils.http import urlencode

from search_engine.models import Corporations


register = template.Library()


@register.inclusion_tag("search_engine/templatetags/corporation_card.html")
def corporation_card(corp: Corporations):
    """
    Render corporation card.
    :param corp: Corporation object.
    :return: Rendered corporation card.
    """
    return {"corp": corp}


@register.inclusion_tag("search_engine/templatetags/page_size_selector.html")
def page_size_selector(page_obj: Page, url: str = "", page_sizes: Iterable = (10, 20, 50, 100), selected_size: int = None, parameter_name: str = "page_size"):
    """
    Render page size selector.
    :param page_obj: Django page object.
    :param url: URL to navigate to for pagination forward and pagination back.
    :param page_sizes:
    :param selected_size: Selected page size.
    :param parameter_name: Name of the paging URL parameter.
    :return: Rendered page size selector.
    """

    # Parse url.
    parts = urlparse(url)

    # Get querystring parameters.
    params = parse_qs(parts.query)

    # build url again.
    url = urlunparse(
        [parts.scheme, parts.netloc, parts.path, parts.params, urlencode(params, doseq=True), parts.fragment]
    )

    if selected_size is None:
        selected_size = page_obj.paginator.per_page

    return {
        "page_obj": page_obj,
        "url": url,
        "page_sizes": page_sizes,
        "selected_size": selected_size,
        "parameter_name": parameter_name,
    }
