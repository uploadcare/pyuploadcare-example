from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, TemplateView
from pyuploadcare.dj.client import get_uploadcare_client
from pyuploadcare.exceptions import UploadcareException


class GroupListView(ListView):
    template_name = "groups/group_list.html"
    paginate_by = 20

    def get_queryset(self):
        uploadcare = get_uploadcare_client()
        return uploadcare.list_file_groups(ordering="-datetime_created")


class GroupInfoView(TemplateView):
    template_name = "groups/group_info.html"

    def get_context_data(self, **kwargs):
        group_id = self.kwargs["group_id"]
        uploadcare = get_uploadcare_client()

        try:
            kwargs["group"] = uploadcare.file_group(group_id)
        except UploadcareException as err:
            messages.error(self.request, f'Unable to get group: {err}')

        return kwargs


class GroupStoreView(View):
    def get(self, request, group_id):
        uploadcare = get_uploadcare_client()

        try:
            group = uploadcare.file_group(group_id)
            group.store()
        except UploadcareException as err:
            messages.error(self.request, f'Unable to store group: {err}')

        return redirect("group_info", group_id)
