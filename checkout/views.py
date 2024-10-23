import stripe
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from fitflexproduct.models import WorkoutProgram as Product
from .forms import OrderForm
from .models import Order, OrderLineItem
from bag.context import bag_contents



def checkout_view(request):
    """
    Handle the checkout process for digital products.
    """
    stripe_public_key =settings.STRIPE_PUBLIC_KEY
    stripe_secret_key =settings.STRIPE_SECRET_KEY
    
    
    if request.method == 'POST':
        bag = request.session.get('bag', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
        }

    else:
        bag = request.session.get('bag', {})
        

        if not bag:
            messages.error(request, "Your bag is currently empty. Please add some workout programs to proceed.")
            return redirect(reverse('products'))  

        current_bag = bag_contents(request)
        total = current_bag['total_price']
        stripe_total = round (total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )

        order_form = OrderForm()
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,

    }

    return render(request, template, context)
