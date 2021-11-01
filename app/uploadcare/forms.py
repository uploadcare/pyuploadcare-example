from django import forms
from django.core.exceptions import ValidationError


class FileUploadForm(forms.Form):
    file = forms.FileField(required=False)
    url = forms.URLField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        if not (cleaned_data.get("file") or cleaned_data.get("url")):
            raise ValidationError("file or url required")
