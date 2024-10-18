from django.shortcuts import render

# Create your views here.
def cart(request):
    """ A view to display cart content"""
    return render(request, 'cart/cart.html')