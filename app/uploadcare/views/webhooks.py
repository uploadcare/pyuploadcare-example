from django.http import Http404
from django.shortcuts import redirect
from django.views import View
from django.views.generic import FormView, ListView, TemplateView
from pyuploadcare.dj.client import get_uploadcare_client

from uploadcare.forms import WebhookForm


class WebhookListView(ListView):
    template_name = "webhooks/webhook_list.html"
    paginate_by = 20

    def get_queryset(self):
        uploadcare = get_uploadcare_client()
        return list(uploadcare.list_webhooks())


class WebhookInfoView(TemplateView):
    template_name = "webhooks/webhook_info.html"

    def get_context_data(self, **kwargs):
        kwargs["webhook"] = get_webhook(self.kwargs["webhook_id"])
        return kwargs


class WebhookDeleteView(View):
    def get(self, request, webhook_id):
        uploadcare = get_uploadcare_client()
        uploadcare.delete_webhook(webhook_id)
        return redirect("webhook_list")


class WebhookCreateView(FormView):
    template_name = "webhooks/webhook_create.html"
    form_class = WebhookForm

    def form_valid(self, form):
        target_url = form.cleaned_data["target_url"]
        is_active = form.cleaned_data["is_active"]
        uploadcare = get_uploadcare_client()
        webhook = uploadcare.create_webhook(target_url=target_url, is_active=is_active)
        return redirect("webhook_info", webhook.id)


class WebhookUpdateView(FormView):
    template_name = "webhooks/webhook_update.html"
    form_class = WebhookForm

    def get_initial(self):
        initial = super().get_initial()

        webhook = get_webhook(self.kwargs["webhook_id"])
        if not webhook:
            raise Http404

        initial["target_url"] = webhook.target_url
        initial["is_active"] = webhook.is_active
        initial["event"] = webhook.event
        return initial

    def form_valid(self, form):
        target_url = form.cleaned_data["target_url"]
        is_active = form.cleaned_data["is_active"]
        event = form.cleaned_data["event"]
        uploadcare = get_uploadcare_client()
        webhook_id = self.kwargs["webhook_id"]
        webhook = uploadcare.update_webhook(
            webhook_id, target_url=target_url, event=event, is_active=is_active
        )
        return redirect("webhook_info", webhook.id)


def get_webhook(webhook_id):
    uploadcare = get_uploadcare_client()
    webhooks = uploadcare.list_webhooks()
    for webhook in webhooks:
        if webhook.id == webhook_id:
            return webhook
