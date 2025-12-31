# app1/signals.py

from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from django.contrib.sessions.models import Session
from .models import Product , Cart
import json
from django.contrib.auth.models import User

@receiver(post_delete, sender=Product)
def remove_product_from_all_carts(sender, instance, **kwargs):

    product_id = str(instance.id)

    sessions = Session.objects.all()

    for session in sessions:
        try:
            data = session.get_decoded()
        except Exception:
            continue

        cart = data.get('cart')

        if cart and product_id in cart:
            del cart[product_id]
            data['cart'] = cart
            session.session_data = Session.objects.encode(data)
            session.save()


@receiver(post_save, sender=User)
def create_cart(sender,instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)