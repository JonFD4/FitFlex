from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from checkout.webhook_handler import StripeWH_Handler
import stripe

@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Print initial info for debugging
    print("Webhook received")
    print(f"Webhook Secret: {wh_secret}")
    print(f"Stripe API Key: {stripe.api_key}")

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    event = None

    try:
        # Print payload and headers for debugging
        print("Payload:", payload)
        print("Signature Header:", sig_header)
        
        # Construct the event
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
        print("Event constructed successfully")
    except ValueError as e:
        # Invalid payload
        print("Invalid payload:", e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print("Invalid signature:", e)
        return HttpResponse(status=400)
    except Exception as e:
        print("General error:", e)
        return HttpResponse(status=400)

    # Set up a webhook handler
    handler = StripeWH_Handler(request)

    # Map webhook events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # Get the webhook type from Stripe
    event_type = event['type']
    print(f"Event type: {event_type}")

    event_handler = event_map.get(event_type, handler.handle_event)


    response = event_handler(event)
    print(f"Handler response: {response.status_code}")
    return response
