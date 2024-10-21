from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from fitflexproduct.models import WorkoutProgram as Product

def bag_view(request):
    """ A view to render bag contents"""
    return render (request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add the specified product to the shopping bag """



    product = Product.objects.get(pk=item_id)
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', [])

    # Convert item_id to integer before appending
    if int(item_id) not in bag:
        bag.append(int(item_id))
        messages.success(request, f'{product.name} is in bag.')
    request.session['bag'] = bag
    return redirect(redirect_url)

def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""
    
    try:
        bag = request.session.get('bag', [])  
        
       
        if item_id in bag:
            bag.remove(item_id)  
            
        request.session['bag'] = bag 
        return HttpResponse(status=200)  
    
    except Exception as e:
        print(f"Error removing item: {e}")  
        return HttpResponse(status=500)  