from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, resolve_url, get_object_or_404
from django.views.generic import TemplateView, View

from .defaults import app_settings, payment_handler
from .models import SslcommerzSession, TransactionStatus


def ipn_response_strategy(request, session):
    return HttpResponse("")


def redirect_response_strategy_factory(redirect_url):
    def response_strategy(request, session):
        url = resolve_url(redirect_url or request.path)
        return redirect(f"{url}?session_id={session.id}")

    return response_strategy


class ResultPageMixin:
    def get_context_data(self, **kwargs):
        session_id = self.request.GET.get("session_id")
        session = get_object_or_404(SslcommerzSession, pk=session_id)
        data = super().get_context_data(**kwargs)
        data["session"] = session
        data["tran_id"] = session.tran_id
        data["success"] = session.status in (
            TransactionStatus.VALID,
            TransactionStatus.VALIDATED,
        )
        return data


class VerifyTransactionMixin:
    def post(self, request):
        return payment_handler.handle_transaction_verification(
            request,
            response_strategy=self.__class__.response_strategy,
        )


class IpnView(VerifyTransactionMixin, View):
    response_strategy = ipn_response_strategy


class SuccessView(VerifyTransactionMixin, ResultPageMixin, TemplateView):
    template_name = app_settings["success_template_name"]
    response_strategy = redirect_response_strategy_factory(
        redirect_url=app_settings["success_url"]
    )


class FailView(VerifyTransactionMixin, ResultPageMixin, TemplateView):
    template_name = app_settings["fail_template_name"]
    response_strategy = redirect_response_strategy_factory(
        redirect_url=app_settings["fail_url"]
    )


class CancelView(VerifyTransactionMixin, ResultPageMixin, TemplateView):
    template_name = app_settings["cancel_template_name"]
    response_strategy = redirect_response_strategy_factory(
        redirect_url=app_settings["cancel_url"]
    )


class SessionDetailView(View):
    def get(self, request):
        session_id = request.GET.get("session_id")
        session = get_object_or_404(SslcommerzSession, pk=session_id)
        session_keys_to_serialize = app_settings["session_keys_to_serialize"]
        response_obj = {key: getattr(session, key) for key in session_keys_to_serialize}
        return JsonResponse(response_obj)
