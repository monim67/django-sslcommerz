import django.dispatch


transaction_complete_signal = django.dispatch.Signal(providing_args=["instance"])
