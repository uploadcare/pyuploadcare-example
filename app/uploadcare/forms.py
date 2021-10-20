from django import forms
from django.core.exceptions import ValidationError
from pyuploadcare.dj.client import get_uploadcare_client
from pyuploadcare.transformations.video import Quality, ResizeMode, VideoFormat


class FileUploadForm(forms.Form):
    file = forms.FileField(required=False)
    url = forms.URLField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        if not (cleaned_data.get("file") or cleaned_data.get("url")):
            raise ValidationError("file or url required")


class WebhookForm(forms.Form):
    target_url = forms.URLField()
    event = forms.ChoiceField(choices=[("file.uploaded", "file.uploaded")])
    is_active = forms.BooleanField(required=False)


class VideoConversionRequestForm(forms.Form):
    file = forms.ChoiceField()
    format = forms.ChoiceField(
        choices=[
            ("", ""),
            (VideoFormat.webm, VideoFormat.webm),
            (VideoFormat.mp4, VideoFormat.mp4),
            (VideoFormat.ogg, VideoFormat.ogg),
        ],
        required=False,
    )
    quality = forms.ChoiceField(
        choices=[
            ("", ""),
            (Quality.normal, Quality.normal),
            (Quality.better, Quality.better),
            (Quality.best, Quality.best),
            (Quality.lighter, Quality.lighter),
            (Quality.lightest, Quality.lightest),
        ],
        required=False,
    )
    resize_mode = forms.ChoiceField(
        choices=[
            ("", ""),
            (ResizeMode.preserve_ratio, ResizeMode.preserve_ratio),
            (ResizeMode.change_ratio, ResizeMode.change_ratio),
            (ResizeMode.scale_crop, ResizeMode.scale_crop),
            (ResizeMode.add_padding, ResizeMode.add_padding),
        ],
        required=False,
    )
    width = forms.IntegerField(required=False)
    height = forms.IntegerField(required=False)

    # Cut
    start_time = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "0:00:00"}), required=False
    )
    length = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "0:00:00"}), required=False
    )

    # Thumbs
    thumbs = forms.IntegerField(required=False)

    store = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uploadcare = get_uploadcare_client()
        files = uploadcare.list_files(ordering="-datetime_uploaded", limit=100)
        self.fields["file"].choices = [(file.uuid, file.filename) for file in files]
