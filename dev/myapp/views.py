from django.dispatch import receiver
from django.views.generic import View

from django_sslcommerz.defaults import payment_handler
from django_sslcommerz.models import SslcommerzSession, TransactionStatus
from django_sslcommerz.signals import transaction_complete_signal


class InitView(View):
    def get(self, request, *args, **kwargs):
        post_data = dict(
            currency="BDT",
            total_amount=100,
            cus_name="Hans",
            cus_email="yawn@yawn.com",
            cus_add1="yawn",
            cus_city="yawn",
            cus_postcode="yawn",
            cus_country="yawn",
            cus_phone="123456",
            shipping_method="NO",
            num_of_item=1,
            product_name="p1",
            product_category="c1",
            product_profile="general",
        )
        post_data.update(request.GET.dict())
        return payment_handler.handle_transaction(request, **post_data)


@receiver(transaction_complete_signal)
def update_transaction_status(sender, instance: SslcommerzSession, **kwargs):
    if instance.status in (TransactionStatus.VALID, TransactionStatus.VALIDATED):
        pass
    elif instance.status == TransactionStatus.FAILED:
        pass
    elif instance.status == TransactionStatus.CANCELLED:
        pass
