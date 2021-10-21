from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
from pyuploadcare.dj.client import get_uploadcare_client
from pyuploadcare.transformations.document import DocumentTransformation
from pyuploadcare.transformations.video import VideoTransformation

from uploadcare.forms import DocumentConversionRequestForm, VideoConversionRequestForm


class VideoConversionRequestView(FormView):
    template_name = "conversions/video/request.html"
    form_class = VideoConversionRequestForm

    def form_valid(self, form):  # noqa: C901
        data = form.cleaned_data

        transformation = VideoTransformation()

        if data["format"]:
            transformation = transformation.format(data["format"])

        if data["quality"]:
            transformation = transformation.quality(data["quality"])

        if data["width"] or data["height"]:
            transformation = transformation.size(data["width"], data["height"], data["resize_mode"])

        if data["start_time"] and data["length"]:
            transformation = transformation.cut(data["start_time"], data["length"])

        if data["thumbs"]:
            transformation = transformation.thumbs(data["thumbs"])

        uploadcare = get_uploadcare_client()

        file_id = data["file"]
        path = transformation.path(file_id)
        response = uploadcare.video_convert_api.convert([path], store=data["store"])

        if response.problems:
            for key, value in response.problems.items():
                messages.error(self.request, f"{key}: {value}")
                return redirect("video_conversion_request")

        token = response.result[0].token
        return redirect("video_conversion_status", token)


class VideoConversionJobStatusView(TemplateView):
    template_name = "conversions/video/status.html"

    def get_context_data(self, **kwargs):
        token = self.kwargs["token"]
        uploadcare = get_uploadcare_client()
        kwargs["job_status"] = uploadcare.video_convert_api.status(token)
        return kwargs


class DocumentConversionRequestView(FormView):
    template_name = "conversions/document/request.html"
    form_class = DocumentConversionRequestForm

    def form_valid(self, form):  # noqa: C901
        data = form.cleaned_data

        transformation = DocumentTransformation()

        if data["format"]:
            transformation = transformation.format(data["format"])

        if data["page"]:
            transformation = transformation.page(data["page"])

        uploadcare = get_uploadcare_client()

        file_id = data["file"]
        path = transformation.path(file_id)
        response = uploadcare.document_convert_api.convert([path], store=data["store"])

        if response.problems:
            for key, value in response.problems.items():
                messages.error(self.request, f"{key}: {value}")
                return redirect("document_conversion_request")

        token = response.result[0].token
        return redirect("document_conversion_status", token)


class DocumentConversionJobStatusView(TemplateView):
    template_name = "conversions/document/status.html"

    def get_context_data(self, **kwargs):
        token = self.kwargs["token"]
        uploadcare = get_uploadcare_client()
        kwargs["job_status"] = uploadcare.document_convert_api.status(token)
        return kwargs
