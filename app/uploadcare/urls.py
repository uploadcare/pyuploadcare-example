"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from uploadcare.views.conversions import (
    DocumentConversionJobStatusView,
    DocumentConversionRequestView,
    VideoConversionJobStatusView,
    VideoConversionRequestView,
)
from uploadcare.views.files import (
    FileBatchActionView,
    FileCopyView,
    FileDeleteView,
    FileInfoView,
    FileListView,
    FileStoreView,
    FileUploadView,
)
from uploadcare.views.groups import GroupInfoView, GroupListView, GroupStoreView
from uploadcare.views.project import ProjectInfoView
from uploadcare.views.webhooks import (
    WebhookCreateView,
    WebhookDeleteView,
    WebhookInfoView,
    WebhookListView,
    WebhookUpdateView,
)


urlpatterns = [
    path("", ProjectInfoView.as_view(), name="project_info"),
    path("files/", FileListView.as_view(), name="file_list"),
    path("files/batch_action/", FileBatchActionView.as_view(), name="files_batch_action"),
    path("files/upload/", FileUploadView.as_view(), name="file_upload"),
    path("files/<str:file_id>/", FileInfoView.as_view(), name="file_info"),
    path("files/<str:file_id>/store/", FileStoreView.as_view(), name="store_file"),
    path("files/<str:file_id>/delete/", FileDeleteView.as_view(), name="delete_file"),
    path("files/<str:file_id>/copy/", FileCopyView.as_view(), name="copy_file"),
    path("groups/", GroupListView.as_view(), name="group_list"),
    path("groups/<str:group_id>/", GroupInfoView.as_view(), name="group_info"),
    path("groups/<str:group_id>/store/", GroupStoreView.as_view(), name="group_store"),
    path("webhooks/", WebhookListView.as_view(), name="webhook_list"),
    path("webhooks/create/", WebhookCreateView.as_view(), name="webhook_create"),
    path("webhooks/<int:webhook_id>/", WebhookInfoView.as_view(), name="webhook_info"),
    path("webhooks/<int:webhook_id>/update/", WebhookUpdateView.as_view(), name="webhook_update"),
    path("webhooks/<int:webhook_id>/delete/", WebhookDeleteView.as_view(), name="webhook_delete"),
    path(
        "conversions/video/request/",
        VideoConversionRequestView.as_view(),
        name="video_conversion_request",
    ),
    path(
        "conversions/video/<str:token>/",
        VideoConversionJobStatusView.as_view(),
        name="video_conversion_status",
    ),
    path(
        "conversions/document/request/",
        DocumentConversionRequestView.as_view(),
        name="document_conversion_request",
    ),
    path(
        "conversions/document/<str:token>/",
        DocumentConversionJobStatusView.as_view(),
        name="document_conversion_status",
    ),
]
