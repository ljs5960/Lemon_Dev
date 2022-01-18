from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from accounts.models import user
from .models import Notice

#  문의하기
def qna(request):
    
    return render(request, 'qna.html')


# 공지사항
def notice(request):
    notice = Notice.objects.all().order_by('-notice_id')

    return render(request, 'notice.html', {'notices': notice})


# 공지사항 상세보기
def notice_detail(request, pk):
    notice = Notice.objects.get(notice_id = pk)
    
    return render(request, 'notice_detail.html', {'notice': notice})