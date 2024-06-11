from django.shortcuts import render
from store.models import Product

def home(request):
    try:
        products = Product.objects.all()
    except Product.DoesNotExist:
        products = None
    return render(request, 'index.html', {'products': products})