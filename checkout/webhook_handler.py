from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order, OrderLineItem
from fitflexproduct.models import WorkoutProgram as Product
from user_profiles.models import UserProfile

import stripe
import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe"""
        intent = event['data']['object']
        pid = intent['id']  
        bag = intent['metadata']['bag']
        save_info = intent['metadata']['save_info']

        first_name = intent['metadata']['first_name']
        last_name = intent['metadata']['last_name']
        email = intent['metadata']['email']
        full_name = f"{first_name} {last_name}"

        billing_details = intent['charges']['data'][0]['billing_details']
        grand_total = round(intent['charges']['data'][0]['amount'] / 100, 2)

        profile = None
        username = intent['metadata']['username']
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_first_name = first_name
                profile.default_last_name = last_name
                profile.email = email
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=full_name,
                    email__iexact=email,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'''Webhook received: {event["type"]} |
                SUCCESS: Verified order already in database''',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=full_name,
                    user_profile=profile,
                    email=email,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )

                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()

            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'''Webhook received: {event["type"]} |
            SUCCESS: Created order in webhook''',
            status=200)


        def handle_payment_intent_payment_failed(self, event):
            """Handle the payment_intent.payment_failed webhook from Stripe"""
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | Payment failed.',
                status=200)
