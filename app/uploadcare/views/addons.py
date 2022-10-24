from logging import getLogger

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView
from pyuploadcare.api.addon_entities import AddonLabels
from pyuploadcare.api.addon_entities import AddonRemoveBGExecutionParams
from pyuploadcare.api.responses import AddonStatus
from pyuploadcare.dj.client import get_uploadcare_client
from pyuploadcare.exceptions import UploadcareException

from uploadcare.forms import AddonAWSRecognitionRequestForm, AddonClamAVScanRequestForm, AddonRemoveBGRequestForm

logger = getLogger()


addon_url_enum_mapping = {
    "aws_recognition": AddonLabels.AWS_LABEL_RECOGNITION,
    "uc_clamav": AddonLabels.CLAM_AV,
    "remove_bg": AddonLabels.REMOVE_BG,
}

addon_url_names = list(addon_url_enum_mapping.keys())

addon_form_mapping = {
    AddonLabels.AWS_LABEL_RECOGNITION: None,
    AddonLabels.CLAM_AV: None,
    AddonLabels.REMOVE_BG: None,
}


class AddonExecutionBaseRequestView(FormView):
    template_name = "addons/addons_execution_setup_base.html"
    form_class = None
    addon_name = None
    addon_url_label = None
    addon_url_name = None

    def get_context_data(self, **kwargs):
        kwargs["addon_url_name"] = self.addon_url_name
        kwargs["addon_url_label"] = self.addon_url_label
        kwargs["form"] = self.form_class()
        return kwargs

    def _get_target_and_params(self, form):
        data = form.cleaned_data
        target_uuid = str(data["target"])
        return target_uuid, {}

    def form_valid(self, form):  # noqa: C901
        target_uuid, params = self._get_target_and_params(form)
        uploadcare = get_uploadcare_client()
        try:
            response = uploadcare.addons_api.execute(target_uuid, self.addon_name)
        except UploadcareException as err:
            messages.error(
                self.request,
                f"Unable to execute {self.addon_name} for file `{target_uuid}`: {err}"
            )
            return redirect(self.addon_url_name)

        request_id = response.request_id
        return redirect("addon_status", self.addon_url_label, target_uuid, request_id)


class AddonExecutionAWSRecognitionRequestView(AddonExecutionBaseRequestView):
    form_class = AddonAWSRecognitionRequestForm
    addon_name = AddonLabels.AWS_LABEL_RECOGNITION
    addon_url_label = "aws_recognition"
    addon_url_name = 'addon_aws_recognition_request'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs["is_aws_recognition"] = True
        return kwargs


class AddonExecutionClamAVRequestView(AddonExecutionBaseRequestView):
    form_class = AddonClamAVScanRequestForm
    addon_name = AddonLabels.CLAM_AV
    addon_url_label = "uc_clamav"
    addon_url_name = 'addon_uc_clamav_virus_scan'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs["is_clamav_virus_scan"] = True
        return kwargs

    def _get_target_and_params(self, form):
        target_uuid, params = super()._get_target_and_params(form)
        params["purge_infected"] = str(form.cleaned_data["purge_infected"])
        return target_uuid, params


class AddonExecutionRemoveBGRequestView(AddonExecutionBaseRequestView):
    form_class = AddonRemoveBGRequestForm
    addon_name = AddonLabels.REMOVE_BG
    addon_url_label = "remove_bg"
    addon_url_name = 'addon_remove_bg'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs["is_remove_bg"] = True
        return kwargs

    def _get_target_and_params(self, form):
        target_uuid, params = super()._get_target_and_params(form)
        params = AddonRemoveBGExecutionParams.parse_obj(form.cleaned_data).dict()
        logger.warning(f"use as params for RemoveBG: {params}")
        return target_uuid, params


class AddonExecutionStatusAndResultsView(TemplateView):
    template_name = "addons/addons_execution_result_base.html"

    def get_context_data(self, **kwargs):
        addon_name = self.kwargs["addon_name"]
        src_file_id = self.kwargs["file_id"]
        addon = addon_url_enum_mapping.get(addon_name)
        kwargs["addon_urls"] = []

        if not addon:
            messages.error(self.request, f"Unable to find addon with name `{addon_name}`, use one of {addon_url_names}")
            kwargs["execution_result"] = {}
            kwargs["addon_urls"] = addon_url_names
            return kwargs

        request_id = self.kwargs["request_id"]
        uploadcare = get_uploadcare_client()
        is_done = False
        kwargs["refresh_link"] = reverse("addon_status", args=[addon_name, src_file_id, request_id])

        try:
            result = uploadcare.addons_api.status(request_id, addon)
            logger.warning(result)
            is_done = result.status == AddonStatus.DONE

            kwargs["execution_result"] = result
            kwargs["is_done"] = is_done
        except UploadcareException as err:
            messages.error(self.request, f"Unable to get addon status: {err}")

        if is_done:
            try:
                file = uploadcare.file(src_file_id)
                logger.warning(file.info["appdata"])

                kwargs["file"] = file
            except UploadcareException as err:
                messages.error(self.request, f"Unable to get file data: {err}")

        return kwargs
