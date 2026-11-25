import threading
from django.db import transaction
from django.test import TestCase
from .models import Item, SignalLog

class DjangoSignalBehaviorTests(TestCase):
    def setUp(self):
        SignalLog.objects.all().delete()
        Item.objects.all().delete()

    def test_q1_signal_receiver_finishes_before_save_returns(self):
        # The post_save receiver creates SignalLog synchronously.
        item = Item(name="synchronous proof")
        item.save()

        # This assertion runs immediately after save() returns.
        # If the receiver were asynchronous, this row would not be guaranteed
        # to exist at this exact point.
        self.assertTrue(
            SignalLog.objects.filter(message__contains=f"Item(id={item.pk})").exists()
        )

    def test_q2_receiver_runs_in_calling_thread(self):
        caller_thread_id = threading.get_ident()
        item = Item(name="same thread proof")
        item.save()

        log = SignalLog.objects.get(message__contains=f"Item(id={item.pk})")
        self.assertIn(f"thread={caller_thread_id}", log.message)

    def test_q3_receiver_write_rolls_back_with_callers_atomic_transaction(self):
        # Both Item.save() and the receiver's SignalLog insert happen inside
        # this atomic transaction. Raising an exception rolls back both.
        try:
            with transaction.atomic():
                item = Item.objects.create(name="transaction proof")
                item_id = item.pk
                self.assertTrue(
                    SignalLog.objects.filter(message__contains=f"Item(id={item_id})").exists()
                )
                raise RuntimeError("Force rollback")
        except RuntimeError:
            pass

        self.assertFalse(Item.objects.filter(name="transaction proof").exists())
        self.assertFalse(
            SignalLog.objects.filter(message__contains=f"Item(id={item_id})").exists()
        )
