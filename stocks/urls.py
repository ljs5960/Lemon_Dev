from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from stocks import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'stocks'

urlpatterns = [
    path('search_stock', views.search_stock, name='search_stock'),
    path('stock', views.stock, name='stock'),
    path('portfolio', views.portfolio, name='portfolio'),
]
