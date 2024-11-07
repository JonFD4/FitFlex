from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Avg  
from django.contrib.auth.decorators import login_required
from .models import WorkoutProgram as Product, WorkoutCategory as Category, DifficultyLevel, Review
from .forms import ReviewForm , ProductForm

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
       
        if 'category' in request.GET:
            category_friendly_name = request.GET.get('category')
            if category_friendly_name:
                selected_category = get_object_or_404(Category, friendly_name__iexact=category_friendly_name)
                products = products.filter(category=selected_category)

        
        if 'difficulty' in request.GET:
            difficulty_name = request.GET.get('difficulty')
            if difficulty_name:
                selected_difficulty = get_object_or_404(DifficultyLevel, name__iexact=difficulty_name)
                products = products.filter(difficulty_level=selected_difficulty)
        
        
        if 'price' in request.GET:
            price_order = request.GET.get('price')
            if price_order == 'low-to-high':
                products = products.order_by('price')  
            elif price_order == 'high-to-low':
                products = products.order_by('-price') 


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
    A view to display product detail, including reviews and review form.
    """
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()  
    average_rating = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0  

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.workout_program = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('product_detail', product_id=product.id)
    else:
        review_form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': review_form,
    }
    return render(request, 'products/product_detail.html', context)


def submit_review(request, product_id):
    """
    Handles the submission of a review for a workout program.
    """
    if request.method == 'POST':
        workout_program = get_object_or_404(Product, pk=product_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

      
        Review.objects.create(
            workout_program=workout_program,
            user=request.user,
            rating=rating,
            comment=comment
        )
        messages.success(request, "Your review has been submitted!")
        return redirect('product_detail', product_id=product_id)

    return redirect('product_detail', product_id=product_id)

# Admin views for managing products
def add_product(request):
    """ View to allow admin to add product to store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add new product. Please add valid information.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }
    return render(request, template, context)

def edit_product(request, product_id):
    """ View to allow admin to edit product """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please add valid information.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

def delete_product(request, product_id):
    """ Allow admin to delete product from store """
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('all_products'))