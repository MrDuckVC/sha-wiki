from django.core.exceptions import ValidationError
from tidylib import tidy_document


def code_validator(value):
    """
    Validate HTML code.

    :param value: HTML code.
    :return: None or raise ValidationError.
    """
    document, errors = tidy_document(value, options={
        "output-xhtml": True,  # Output XHTML.
        "numeric-entities": True,  # Use numeric entities instead of named entities.
        "doctype": "omit",  # To ignore <!DOCTYPE html> missing warning.
        "show-body-only": True,  # To ignore inserting implicit <body> tag and missing <title> tag warnings.
    })
    if errors:
        raise ValidationError(errors)
