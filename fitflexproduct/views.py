from django.shortcuts import render, get_object_or_404
from .models import WorkoutProgram as Product, WorkoutProgram, WorkoutCategory as Category


def all_products(request):
    """
    A view to display all products, allow sorting and search queries
    """
    products= Product.objects.all()
    categories = Category.objects.all()

    context={
        'products':products,
        'categories': categories,
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