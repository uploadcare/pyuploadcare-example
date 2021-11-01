from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
from pyuploadcare.dj.client import get_uploadcare_client
from pyuploadcare.transformations.video import VideoTransformation

from uploadcare.forms import VideoConversionRequestForm


class VideoConversionRequestView(FormView):
    template_name = "conversions/video/request.html"
    form_class = VideoConversionRequestForm

    def form_valid(self, form):  # noqa: C901
        data = form.cleaned_data

        transformation = VideoTransformation()

        target_format = data.get("format")
        if target_format:
            transformation = transformation.format(target_format)

        quality = data.get("quality")
        if quality:
            transformation = transformation.quality(quality)

        resize_mode = data.get("resize_mode")
        width = data.get("width")
        height = data.get("height")
        if width or height:
            transformation = transformation.size(width, height, resize_mode)

        start_time = data.get("start_time")
        length = data.get("length")
        if start_time and length:
            transformation = transformation.cut(start_time, length)

        thumbs = data.get("thumbs")
        if thumbs:
            transformation = transformation.thumbs(thumbs)

        store = data.get("store")

        uploadcare = get_uploadcare_client()

        file_id = data["file"]
        path = transformation.path(file_id)
        response = uploadcare.video_convert_api.convert([path], store=store)

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
