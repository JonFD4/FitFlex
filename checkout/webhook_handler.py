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

        # Check for existing order
        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    order_number=intent.metadata.order_number,  # Use metadata for order number
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200
            )
        else:
            order = None
            try:
                # Create the order
                order = Order.objects.create(
                    order_number=intent.metadata.order_number,
                    email=intent.metadata.email,  
                    is_paid=True, 
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
                    

                self.send_confirmation_email(order)

            except Exception as e:
                if order:
                    order.delete()  # Clean up if there's an error
                # Log the error for debugging
                print(f'Error creating order: {str(e)}') 
                return HttpResponse(
                    content='Webhook received: {} | ERROR: Order processing failed.'.format(event["type"]),
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
        
    def send_confirmation_email(self, order):
        """Send confirmation email to the customer."""
        subject = f'Order Confirmation - {order.order_number}'
        message = f'Thank you for your order! Your order number is {order.order_number}.'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.email], 
        )
