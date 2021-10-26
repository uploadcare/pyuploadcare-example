from django.views.generic import TemplateView
from pyuploadcare.dj.client import get_uploadcare_client


class ProjectInfoView(TemplateView):
    template_name = "project_info.html"

    def get_context_data(self, **kwargs):
        uploadcare = get_uploadcare_client()
        kwargs["project"] = uploadcare.get_project_info()
        return kwargs
