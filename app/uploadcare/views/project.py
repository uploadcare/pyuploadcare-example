from django.contrib import messages
from django.views.generic import TemplateView
from pyuploadcare.dj.client import get_uploadcare_client


from pyuploadcare.exceptions import UploadcareException


class ProjectInfoView(TemplateView):
    template_name = "projects/project_info.html"

    def get_context_data(self, **kwargs):
        uploadcare = get_uploadcare_client()

        try:
            kwargs["project"] = uploadcare.get_project_info()
        except UploadcareException as err:
            messages.error(self.request, f'Unable to get project info: {err}')
            kwargs["project"] = None

        return kwargs
