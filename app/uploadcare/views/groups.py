from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView
from pyuploadcare.dj.client import get_uploadcare_client


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
        kwargs["group"] = uploadcare.file_group(group_id)
        return kwargs


def group_store(request, group_id):
    uploadcare = get_uploadcare_client()
    group = uploadcare.file_group(group_id)
    group.store()
    return redirect("group_info", group_id)
