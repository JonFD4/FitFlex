from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from fitflexproduct.models import WorkoutProgram as Product  
# 
def cart(request):
    """ A view to display cart content"""
    return render(request, 'cart/cart.html')



def add_to_cart(request, item_id):
    """ Add digital products to the cart with a default quantity of 1 """
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    # Get the product being added to the cart
    product = get_object_or_404(Product, pk=item_id)

    # Check if the product is already in the cart
    if item_id in cart:
        messages.info(request, 'This item is already in your cart.')
    else:
        # Add the product details, including price, and set quantity to 1
        cart[item_id] = {
            'name': product.name,
            'price': float(product.price),  
            'image_url': product.image.url,  
            'quantity': 1,  
        }
        messages.success(request, f'{product.name} added to your cart!')

    # Update the cart in the session
    request.session['cart'] = cart
    request.session.modified = True  

    return redirect(redirect_url)
