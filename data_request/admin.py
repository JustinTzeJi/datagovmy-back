from typing import Any

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from modeltranslation.admin import TranslationAdmin

from data_catalogue.models import DataCatalogueMeta
from data_request.models import DataRequest


class DataRequestAdminForm(forms.ModelForm):
    valid_catalogue_meta_ids = forms.ModelMultipleChoiceField(
        queryset=DataCatalogueMeta.objects.all(),
        widget=FilteredSelectMultiple("Valid Catalogue Meta IDs", False),
        required=False,
    )

    class Meta:
        model = DataRequest
        fields = "__all__"

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        valid_catalogue_meta_ids = cleaned_data.get("valid_catalogue_meta_ids")

        # Check if more than one DataCatalogueMeta is selected only if status is "rejected"
        if status == "data_published" and not valid_catalogue_meta_ids.exists():
            raise forms.ValidationError(
                {
                    "valid_catalogue_meta_ids": 'At least one Data Catalogue must be selected for "data_published" status.'
                }
            )
        return cleaned_data


class DataRequestAdmin(TranslationAdmin):
    readonly_fields = [
        "ticket_id",
        "name",
        "email",
        "institution",
        "agency",
        "purpose_of_request",
    ]
    form = DataRequestAdminForm
    list_filter = ["status"]  # Add the 'status' field to enable filtering

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.pk:
            form.base_fields[
                "valid_catalogue_meta_ids"
            ].initial = obj.published_data.values_list("pk", flat=True)
        if self.has_change_permission(request):
            # data request manager must update both en and ms fields
            form.base_fields["dataset_title_ms"].required = True
            form.base_fields["dataset_description_ms"].required = True

        return form

    def has_change_permission(self, request, obj=None):
        # Allow users in the "Data Request Manager" group to change the object
        return request.user.groups.filter(name="Data Request Manager").exists()

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        super().save_model(request, obj, form, change)
        obj.published_data.set(form.cleaned_data.get("valid_catalogue_meta_ids"))


admin.site.register(DataRequest, DataRequestAdmin)
