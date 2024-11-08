from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse

def index(request):
    """A view to return the index page"""
    return render(request, 'home/index.html')

def contact_view(request):
    if request.method == 'POST':
      
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        category = request.POST.get('category')
        message = request.POST.get('message')
        messages.success(request, "Thank you for contacting us! We'll get back to you soon.")
        return redirect(reverse('contact'))
    
    return render(request, 'home/index.html')

def newsletter_subscribe(request):
    if request.method == 'POST' and 'email' in request.POST:
        email = request.POST['email']
        messages.success(request, f'Thank you for subscribing!')
    return render(request, 'home/index.html')