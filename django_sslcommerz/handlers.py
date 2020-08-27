import logging
from functools import wraps

from django.conf import settings
from django.shortcuts import redirect, render, reverse
from sslcommerz_sdk.exceptions import SslcommerzException
from sslcommerz_sdk.handlers import PaymentHandler, sslcommerz_exception_context
from sslcommerz_sdk.querysets.django import DjangoQuerySetBuilder

from .apps import app_settings
from .models import SslcommerzSession
from .signals import transaction_complete_signal

logger = logging.getLogger(__name__)


def get_absolute_uri(request, url_name):
    return request.build_absolute_uri(reverse(url_name))


def sslcommerz_exception_handler(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except SslcommerzException as ex:
            if settings.DEBUG:
                raise
            logger.exception(ex)
            return render(
                request,
                app_settings["error_template_name"],
                {"success": False, "tran_id": ex.tran_id},
            )

    return wrapper


class DjangoPaymentHandler(PaymentHandler):
    def __init__(self, store):
        super().__init__(
            model=SslcommerzSession,
            queryset_builder=DjangoQuerySetBuilder,
            store=store,
        )

    @sslcommerz_exception_handler
    def handle_transaction(self, request, **kwargs):
        _, session = self.get_or_create_session(
            ipn_url=get_absolute_uri(request, "django_sslcommerz:ipn"),
            success_url=get_absolute_uri(request, "django_sslcommerz:success"),
            fail_url=get_absolute_uri(request, "django_sslcommerz:fail"),
            cancel_url=get_absolute_uri(request, "django_sslcommerz:cancel"),
            **kwargs,
        )
        return redirect(session.redirect_url)

    @sslcommerz_exception_handler
    def handle_transaction_verification(self, request, response_strategy):
        payload = request.POST.dict()
        session, verified_just_now = self.verify_transaction(payload)
        with sslcommerz_exception_context(session.tran_id):
            if verified_just_now:
                transaction_complete_signal.send(
                    sender=self.__class__, instance=session
                )
            return response_strategy(request, session)
