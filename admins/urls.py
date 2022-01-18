from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name='admins'

urlpatterns = [
    path('qna', views.qna), # 문의하기
    path('notice', views.notice, name='notice'), # 공지사항
    path('notice/<int:pk>', views.notice_detail, name='notice_detail'), # 공지사항 상세보기
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)