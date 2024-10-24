import stripe
import json

from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST

from fitflexproduct.models import WorkoutProgram as Product
from .forms import OrderForm
from .models import Order, OrderLineItem
from bag.context import bag_contents  # Import the bag_contents function


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, ('Sorry, your payment cannot be '
                                 'processed right now. Please try '
                                 'again later.'))
        return HttpResponse(content=e, status=400)

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    current_bag = bag_contents(request)
    grand_total = current_bag['grand_total']  
    discounted_total = current_bag['total_price']

    if request.method == 'POST':
        # Retrieve the bag from session
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))


        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
        }
        order_form = OrderForm(form_data)
        print(form_data)
        
        if order_form.is_valid():
            print('form is valid')
            print(order_form.errors) 

            order = order_form.save(commit=False)
            print(order)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.grand_total = grand_total
            order.order_total = discounted_total
            order.save()


            try:
                for item_id in bag:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        lineitem_price=product.price
                    )
                    order_line_item.save()
            except Product.DoesNotExist:
                messages.error(request, (
                    "One of the products in your bag wasn't found in our database. "
                    "Please contact us for assistance!")
                )
                order.delete()
                return redirect(reverse('bag'))

            # Store info for future use
            request.session['save_info'] = 'save-info' in request.POST

            # Redirect to a success page 
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double-check your information.')

    else:
 
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('all_products'))


      
        
        stripe_total = round(discounted_total * 100) 
        
        

        # Create a payment intent for Stripe
        stripe.api_key = stripe_secret_key
        try:
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )
        except stripe.error.StripeError as e:
            messages.error(request, f'Stripe error occurred: {str(e)}')
            return redirect(reverse('bag'))

       
        order_form = OrderForm()

    # Warn if Stripe public key is missing
    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Please set it in your environment.')

    # Prepare template context
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,  # Pass the client secret to the template
        
    }

    return render(request, template, context)



def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email with a link to purchased product will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)