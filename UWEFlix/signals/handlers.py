from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from UWEFlix.models import Customer

## this is imported to the app file, and is run when the app is ready (initialised)
## this method allows us to replace the get_or_create
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']:
        Customer.objects.create(user=kwargs['instance'])