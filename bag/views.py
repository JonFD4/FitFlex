from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from fitflexproduct.models import WorkoutProgram as Product

def bag_view(request):
    """ A view to render bag contents"""
    return render (request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add the specified product to the shopping bag """



    product = get_object_or_404(Product,pk=item_id)
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', [])

    # Convert item_id to integer before appending
    if int(item_id) in bag:
        messages.info(request, f'{product.name} is already in your bag.')
        
    else:
        bag.append(int(item_id))
        messages.success(request, f'{product.name} has been added to your bag.')
    request.session['bag'] = bag
    return redirect(redirect_url)

def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""
    product = get_object_or_404(Product,pk=item_id)
    try:
        bag = request.session.get('bag', [])  
        
       
        if item_id in bag:
            bag.remove(item_id)  
            messages.success(request, f'{product.name} has been removed from bag.')
        request.session['bag'] = bag 
        return HttpResponse(status=200)  
    
    except Exception as e: 
        return HttpResponse(status=500)  