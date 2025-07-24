from django.db.models import TextField
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget


class BaseAdmin(ModelAdmin):
    ordering = ('-created_at',)
    list_filter = ['is_active']
    compressed_fields = True

    # Warn before leaving unsaved changes in changeform
    warn_unsaved_form = True

    # Preprocess content of readonly fields before render
    readonly_preprocess_fields = {
        "model_field_name": "html.unescape",
        "other_field_name": lambda content: content.strip(),
    }

    # Display submit button in filters
    list_filter_submit = True

    # Custom actions
    actions_list = []  # Displayed above the results list
    actions_row = []  # Displayed in a table row in results list
    actions_detail = []  # Displayed at the top of for in object detail
    actions_submit_line = []  # Displayed near save in object detail

    formfield_overrides = {
        TextField: {
            "widget": WysiwygWidget,
        }
    }
