from django import forms
from django.core.exceptions import ValidationError
from pyuploadcare.dj.client import get_uploadcare_client
from pyuploadcare.transformations.document import DocumentFormat
from pyuploadcare.transformations.video import Quality, ResizeMode, VideoFormat
from pyuploadcare.dj.forms import ImageField, FileGroupField, FileWidget

from uploadcare.models import Post


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
        choices=[("", "")] + [(key, key) for key in VideoFormat],
        required=False,
    )
    quality = forms.ChoiceField(
        choices=[("", "")] + [(key, key) for key in Quality],
        required=False,
    )
    resize_mode = forms.ChoiceField(
        choices=[("", "")] + [(key, key) for key in ResizeMode],
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


class DocumentConversionRequestForm(forms.Form):
    file = forms.ChoiceField()
    format = forms.ChoiceField(
        choices=[("", "")] + [(key, key) for key in DocumentFormat],
        required=False,
    )
    page = forms.IntegerField(required=False)
    store = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uploadcare = get_uploadcare_client()
        files = uploadcare.list_files(ordering="-datetime_uploaded", limit=100)
        self.fields["file"].choices = [(file.uuid, file.filename) for file in files]


class PostForm(forms.ModelForm):
    logo = ImageField()
    attachments = FileGroupField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'logo', 'attachments']
