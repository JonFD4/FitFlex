from django.shortcuts import render

def custom_404(request, exception):
    # Render the 404 page with custom template
    return render(request, '404.html', status=404)