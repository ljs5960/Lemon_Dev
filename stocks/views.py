from django.shortcuts import render

# Create your views here.


def search_stock(request):
    return render(request, 'search_stock.html')

def stock(request):
    return render(request, 'stock.html')

def portfolio(request):
    return render(request, 'portfolio.html')