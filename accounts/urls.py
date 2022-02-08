from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

#from .views import LemonUserAPI
app_name='accounts'

urlpatterns = [
    path('main', views.main, name='main'),
    path('signup', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('authaccounts/kakao/login', views.KakaoSignInView, name='KakaoSignInView'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)