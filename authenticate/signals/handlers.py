from django.dispatch import receiver
from UWEFlix.signals import order_created

@receiver(order_created)
def on_order_created(sender, **kwargs):
    print(kwargs['order'])