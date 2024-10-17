from django.shortcuts import render, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q 
from .models import WorkoutProgram as Product, WorkoutProgram, WorkoutCategory as Category, DifficultyLevel


def all_products(request):
    """
    A view to display all products, allow sorting and search queries
    """
    products= Product.objects.all()
    categories = Category.objects.all()
    difficulty_levels = DifficultyLevel.objects.all()
    query = None
    selected_category = None
   
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,"Enter a search criteria")
                return redirect(reverse('products'))
        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products= products.filter(queries)

    # Category filter functionality
        if 'category' in request.GET:
                selected_category = request.GET('category').split(',')
                if selected_category:  # Check if category is not None
                    products = products.filter(category__friendly_name__iexact=selected_category)

            
    context={
        'products':products,
        'categories': categories,
        'difficulty_levels': difficulty_levels,
        'search_term': query,
        'selected_category': selected_category,
    }
    return render(request, 'products/products.html', context)
    
def product_detail(request, product_id):
        """
        A view to display product detail
        """
        product = get_object_or_404(Product, pk=product_id)
        context={
            'product':product
        }
        return render(request, 'products/product_detail.html', context)