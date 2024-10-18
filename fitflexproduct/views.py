from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import WorkoutProgram as Product, WorkoutCategory as Category, DifficultyLevel

def all_products(request):
    """
    A view to display all products, allow sorting and search queries,
    and filter by category or difficulty level.
    """
    products = Product.objects.all()
    categories = Category.objects.all()
    difficulty_levels = DifficultyLevel.objects.all()
    query = None
    selected_category = None
    selected_difficulty = None
    price_order = None


    if request.GET:
        # Filtering by category
        if 'category' in request.GET:
            category_friendly_name = request.GET.get('category')
            if category_friendly_name:
                # Try to get the category based on the friendly name (case-insensitive)
                selected_category = get_object_or_404(Category, friendly_name__iexact=category_friendly_name)
                products = products.filter(category=selected_category)

        # Filtering by difficulty level (optional if needed)
        if 'difficulty' in request.GET:
            difficulty_name = request.GET.get('difficulty')
            if difficulty_name:
                selected_difficulty = get_object_or_404(DifficultyLevel, name__iexact=difficulty_name)
                products = products.filter(difficulty_level=selected_difficulty)
        
         # Filtering by price
        if 'price' in request.GET:
            price_order = request.GET.get('price')
            if price_order == 'low-to-high':
                products = products.order_by('price')  # Sort by price ascending
            elif price_order == 'high-to-low':
                products = products.order_by('-price') 

        # Handling search queries
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Enter a search criteria")
                return redirect(reverse('all_products'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'categories': categories,
        'difficulty_levels': difficulty_levels,
        'search_term': query,
        'selected_category': selected_category,
        'selected_difficulty': selected_difficulty,
        'price_order': price_order,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    A view to display product detail
    """
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)
