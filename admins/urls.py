from django.urls import path, include
from . import views

app_name='admins'
urlpatterns = [
    path('qna/write', views.qna_write),
    path('qna/list', views.qna_list),
]