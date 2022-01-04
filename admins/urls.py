from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='admins'

urlpatterns = [
    path('qna/<int:pk>/', views.qna),
    path('qna/write', views.qna_write),
    path('qna/list', views.qna_list),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)