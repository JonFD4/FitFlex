from datetime import datetime
from decimal import Decimal
from django.utils import timezone
from fitflexproduct.models import WorkoutProgram as Product
from django.shortcuts import get_object_or_404

def is_october(month):
    """Check if the given month is October."""
    return month == 10  


def cart_contents(request):
    """Retrieve the cart contents, including total price, discount, and any applicable details."""
    cart_items = []
    total_price = Decimal('0.00') 
    product_count = 0
    discount = Decimal('20.00') 
    current_date = timezone.now()
    current_month = current_date.month

    
    cart = request.session.get('cart', {})

   
    for item_id, item_data in cart.items():
       
        product = Product.objects.get(id=item_id)
        

        item_total_price = product.price  

    
        cart_items.append({
            'product': product,
            'total_price': item_total_price,
        })

       
        total_price += item_total_price
        product_count += 1


    october_discount_applies = is_october(current_month)


    if october_discount_applies:
        discount_amount = (discount / 100) * total_price
        discounted_total = total_price - discount_amount
    else:
        discount_amount = 0
        discounted_total = total_price

    grand_total = total_price  

    context = {
        'cart_items': cart_items, 
        'total_price': discounted_total,  
        'grand_total': grand_total,  
        'discount_amount': discount_amount,  
        'discount_percent': discount if october_discount_applies else 0,  
        'october_discount_applies': october_discount_applies, 
    }
    
    return context