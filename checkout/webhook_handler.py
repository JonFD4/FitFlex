from django.http import HttpResponse
from .models import Order, OrderLineItem
from fitflexproduct.models import WorkoutProgram as Product
from django.conf import settings
import stripe
import json
import time

class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request
    
    def handle_event(self, event):
        """Handle a generic/unknown/unexpected webhook event"""
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe"""
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        email = intent.metadata.email
        full_name = intent.metadata.full_name  # Ensure this exists
        save_info = intent.metadata.save_info
        
        # Retrieve the latest charge to access billing details and amount
        try:
            stripe_charge = stripe.Charge.retrieve(intent.latest_charge)
        except stripe.error.StripeError as e:
            # Handle the error and log it
            print(f"Stripe error: {e}")
            return HttpResponse(status=500)

        billing_details = stripe_charge.billing_details
        grand_total = round(stripe_charge.amount / 100, 2)  

        # Check if the order already exists
        try:
            order = Order.objects.get(
                email__iexact=email,
                stripe_pid=pid,
                full_name__iexact=full_name,
                grand_total=grand_total,
                original_bag=bag,
            )
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200
            )
        except Order.DoesNotExist:
            order = None

        try:
            # Create the order
            order = Order.objects.create(
                email=email,
                is_paid=True,
                stripe_pid=pid,
                grand_total=grand_total,
                original_bag=bag,
            )

            # Process the order items
            for item_id, item_data in json.loads(bag).items():
                product = Product.objects.get(id=item_id)
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    lineitem_price=product.price,
                )
                order_line_item.save()

           
        except Exception as e:
            if order:
                order.delete()  # Clean up if there's an error
            # Log the error for debugging
            print(f'Error processing order: {str(e)}')
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: Order processing failed.',
                status=500
            )

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """Handle the payment_intent.payment_failed webhook from Stripe"""
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | Payment failed.',
            status=200
        )
