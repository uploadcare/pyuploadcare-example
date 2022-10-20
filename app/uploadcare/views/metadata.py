from logging import getLogger

from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.views.generic import FormView
from pyuploadcare.dj.client import get_uploadcare_client
from pyuploadcare.exceptions import UploadcareException

from uploadcare.forms import FileMetadataKeyValueForm


logger = getLogger()


class FileMetadataKeyDeleteView(View):
    def get(self, request, file_id, md_key):
        uploadcare = get_uploadcare_client()

        try:
            logger.debug(f"Try to delete key `{md_key}` for file `{file_id}`")
            uploadcare.metadata_api.delete_key(file_id, mkey=md_key)
        except UploadcareException as err:
            messages.error(
                self.request,
                f"Unable to delete metadata key `{md_key}` for file `{file_id}`: {err}",
            )

        return redirect("file_info", file_id)


class FileMetadataKeyUpdateView(FormView):
    form_class = FileMetadataKeyValueForm

    def form_valid(self, form):
        md_key = form.cleaned_data["meta_key"]
        md_value = form.cleaned_data["meta_value"]
        file_id = self.kwargs["file_id"]

        uploadcare = get_uploadcare_client()

        try:
            logger.debug(
                f"Try to update key `{md_key}` for file `{file_id}` with value `{md_value}`"
            )
            uploadcare.metadata_api.update_or_create_key(file_id, md_key, md_value)

        except UploadcareException as err:
            messages.error(self.request, f"Unable to upload file: {err}")
            return redirect("file_list")

        return redirect("file_info", file_id)

    def form_invalid(self, form):
        logger.warning(f"Failed to validate form {form.cleaned_data}: {form.errors}")
        messages.error(self.request, f"Data is corrupted: {form.errors}")
        file_id = self.kwargs["file_id"]
        return redirect("file_info", file_id)
