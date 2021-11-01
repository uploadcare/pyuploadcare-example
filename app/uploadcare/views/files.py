from django.shortcuts import redirect
from django.views import View
from django.views.generic import FormView, ListView, TemplateView
from pyuploadcare.dj.client import get_uploadcare_client

from uploadcare.forms import FileUploadForm


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


class FileStoreView(View):
    def get(self, request, file_id):
        uploadcare = get_uploadcare_client()
        file = uploadcare.file(file_id)
        file.store()
        return redirect("file_list")


class FileDeleteView(View):
    def get(self, request, file_id):
        uploadcare = get_uploadcare_client()
        file = uploadcare.file(file_id)
        file.delete()
        return redirect("file_list")


class FileCopyView(View):
    def get(self, request, file_id):
        uploadcare = get_uploadcare_client()
        file = uploadcare.file(file_id)
        new_file = file.create_local_copy()
        return redirect("file_info", new_file.uuid)


class FileUploadView(FormView):
    template_name = "files/file_upload.html"
    form_class = FileUploadForm

    def form_valid(self, form):
        file = form.cleaned_data["file"]
        url = form.cleaned_data["url"]
        uploadcare = get_uploadcare_client()

        if file:
            file = uploadcare.upload(file, size=file.size)
        else:
            file = uploadcare.upload(url)

        return redirect("file_info", file.uuid)


class FileBatchActionView(View):
    def post(self, request):
        batch_methods = {
            "store": self._store_files,
            "delete": self._delete_files,
            "create_group": self._create_group,
        }
        action = request.POST["action"]
        files = request.POST.getlist("files")
        uploadcare = get_uploadcare_client()
        method = batch_methods[action]
        return method(uploadcare, files)

    def _store_files(self, uploadcare, files):
        uploadcare.store_files(files)
        return redirect("file_list")

    def _delete_files(self, uploadcare, files):
        uploadcare.delete_files(files)
        return redirect("file_list")

    def _create_group(self, uploadcare, files):
        files = [uploadcare.file(file) for file in files]
        group = uploadcare.create_file_group(files)
        return redirect("group_info", group.id)
