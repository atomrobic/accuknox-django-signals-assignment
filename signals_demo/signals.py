import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item, SignalLog

@receiver(post_save, sender=Item)
def item_post_save_receiver(sender, instance, created, **kwargs):
    # This database write is deliberately performed inside the receiver.
    SignalLog.objects.create(
        message=f"Receiver ran for Item(id={instance.pk}) "
                f"in thread={threading.get_ident()}"
    )
