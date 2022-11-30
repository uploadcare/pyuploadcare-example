from django import forms
from django.core.exceptions import ValidationError
from pyuploadcare.api.metadata import META_KEY_MAX_LEN, META_VALUE_MAX_LEN, key_matcher
from pyuploadcare.dj.client import get_uploadcare_client
from pyuploadcare.dj.forms import FileGroupField, ImageField
from pyuploadcare.transformations.document import DocumentFormat
from pyuploadcare.transformations.video import Quality, ResizeMode, VideoFormat

from uploadcare.models import Post


class FileUploadForm(forms.Form):
    file = forms.FileField(required=False)
    url = forms.URLField(required=False)
    store = forms.ChoiceField(
        choices=[("auto", "auto"), ("yes", "yes"), ("no", "no")]
    )

    def clean(self):
        cleaned_data = super().clean()

        if not (cleaned_data.get("file") or cleaned_data.get("url")):
            raise ValidationError("file or url required")

        converted_store = {"yes": True, "no": False, "auto": None}.get(cleaned_data["store"])
        cleaned_data["store"] = converted_store

        return cleaned_data


class FileMetadataKeyValueForm(forms.Form):
    meta_key = forms.RegexField(max_length=META_KEY_MAX_LEN, regex=key_matcher)
    meta_value = forms.CharField(max_length=META_VALUE_MAX_LEN)


class WebhookForm(forms.Form):
    target_url = forms.URLField()
    event = forms.ChoiceField(
        choices=[("file.uploaded", "file.uploaded"), ("file.infected", "file.infected")]
    )
    is_active = forms.BooleanField(required=False)
    signing_secret = forms.CharField(required=False)


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
        fields = ["title", "content", "logo", "attachments"]


class AddonBaseRequestForm(forms.Form):
    target = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uploadcare = get_uploadcare_client()
        files = uploadcare.list_files(ordering="-datetime_uploaded", limit=100)
        self.fields["target"].choices = [(file.uuid, file.filename) for file in files]


class AddonAWSRecognitionRequestForm(AddonBaseRequestForm):
    pass


class AddonClamAVScanRequestForm(AddonBaseRequestForm):
    purge_infected = forms.BooleanField(required=False)


class AddonRemoveBGRequestForm(AddonBaseRequestForm):
    crop = forms.BooleanField(required=False)
    crop_margin = forms.RegexField(required=False, regex=r"^(?:0|[0-9]+px|[0-9]+%)$")
    scale = forms.CharField(required=False)
    add_shadow = forms.BooleanField(required=False)
    type_level = forms.ChoiceField(
        required=False, choices=[(i, i) for i in ["none", "1", "2", "latest"]]
    )
    type = forms.ChoiceField(
        required=False, choices=[(i, i) for i in ["auto", "person", "product", "car"]]
    )
    semitransparency = forms.BooleanField(required=False)
    channels = forms.ChoiceField(required=False, choices=[(i, i) for i in ["rgba", "alpha"]])
    roi = forms.RegexField(
        required=False, regex=r"^(?:(?:(?:\d+px ){3}\d+px)|(?:(?:\d+% ){3}\d+%))$"
    )
    position = forms.RegexField(required=False, regex=r"^(?:origin|center|\d+%|\d+% \d+%)$")
