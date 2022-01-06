from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from accounts.models import user
from .models import Qna
from .forms import QnaForm


def qna(request):

    return render(request, 'qna.html')


def qna_write(request):
    if request.method == 'POST':
        form = QnaForm(request.POST)
        if form.is_valid():
            user = request.user.user_id
            status = 0  # 0->상담대기, 1->상담완료
            category = form.cleaned_data['category']
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            file = form.cleaned_data['file']
            form.save()
            
            return redirect('/qna/list')
    else:
        form = QnaForm()
        
    return render(request, 'qna_write.html', {'form': form})


def qna_list(request):
    user = request.user.user_id
    qna_list = Qna.objects.filter(user_id=user).order_by('-qna_date')
    
    return render(request, 'qna_list.html', {'qna_list': qna_list})