from django import forms

from search_engine.models import Prefectures


class SearchForm(forms.Form):
    # TODO: Search as user types and remove submit button.
    search_field = forms.CharField(max_length=256, required=False, label="", help_text="Search by number, name or address.")


class ButtonCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = "search_engine/widgets/button_checkbox_select.html"
    option_template_name = "search_engine/widgets/button_checkbox_option.html"

    # class name for input tag
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs["class"] = "btn-check me-2"
        self.attrs["autocomplete"] = "off"


class TagsMultipleChoiceField(forms.MultipleChoiceField):
    widget = ButtonCheckboxSelectMultiple()


class PrefectureForm(forms.Form):
    prefecture = TagsMultipleChoiceField(
        choices=[
            (f"{prefecture.code}", f"{prefecture.name} ({prefecture.en_name})" if prefecture.en_name else f"{prefecture.name}")
            for prefecture in Prefectures.objects.all()
        ],
        required=False,
        label="",
        help_text="Search by prefecture.",
    )
