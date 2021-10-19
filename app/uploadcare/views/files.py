from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView, TemplateView
from pyuploadcare.dj.client import get_uploadcare_client


class FileListView(ListView):
    template_name = "files/file_list.html"
    paginate_by = 20

    def get_queryset(self):
        uploadcare = get_uploadcare_client()
        files = uploadcare.list_files(ordering="-datetime_uploaded")

        # workaround: API return total=0 for demo account
        if not files.count():
            files._count = 100

        return files


class FileInfoView(TemplateView):
    template_name = "files/file_info.html"

    def get_context_data(self, **kwargs):
        uploadcare = get_uploadcare_client()
        file_id = self.kwargs["file_id"]
        kwargs["file"] = uploadcare.file(file_id)
        return kwargs


def store_file(request, file_id):
    uploadcare = get_uploadcare_client()
    file = uploadcare.file(file_id)
    file.store()
    return redirect("file_list")


def delete_file(request, file_id):
    uploadcare = get_uploadcare_client()
    file = uploadcare.file(file_id)
    file.delete()
    return redirect("file_list")


@require_POST
def files_batch_action(request):
    batch_methods = {
        "store": _store_files,
        "delete": _delete_files,
        "create_group": _create_group,
    }
    action = request.POST["action"]
    files = request.POST.getlist("files")
    method = batch_methods.get(action)
    return method(files)


def _store_files(files):
    uploadcare = get_uploadcare_client()
    uploadcare.store_files(files)
    return redirect("file_list")


def _delete_files(files):
    uploadcare = get_uploadcare_client()
    uploadcare.delete_files(files)
    return redirect("file_list")


def _create_group(files):
    uploadcare = get_uploadcare_client()
    files = [uploadcare.file(file) for file in files]
    group = uploadcare.create_file_group(files)
    return redirect("group_info", group.id)
