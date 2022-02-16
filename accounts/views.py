import email
from unittest import result
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.contrib import auth

from django.contrib.auth import login, authenticate, get_user_model

from django.contrib.auth import views as auth_views
from django.contrib.auth import views

from django.contrib.auth.models import User
from .models import user
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timedelta
from django.contrib.auth.decorators import login_required
# Create your views here.
import datetime
from django.db.models import Sum, Count
import os, json
from django.conf import settings
from django.views.generic import View
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .socialviews import KakaoSignInView, KakaoSignInCallbackView
from django.core.mail.message import EmailMessage
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.urls import reverse_lazy
from datetime import datetime
import datetime, requests
URL_LOGIN = '/login'


def user_Confirm(request):
    if request.method == "POST":
        uid = request.POST.get('uid', None)
        print(uid)
        email = request.POST.get('email', None)
        print(email)
        id = User.objects.filter(uid = uid).values('uid')
        print(id)
        email = User.objects.filter(email = email).values('email')
        print(email)
        if id:
            id = '중복'
        else:
            id ='없음'
        print(id)
        if email:
            email='중복'
        else:
            email='없음'
        print(email)
        mesage1 = list(id)
        print(mesage1)
        mesage2 = list(email)
        print(mesage2)

        go = { 'msg':mesage1,
               'msg':mesage2}
        print(go)
        return JsonResponse(go)



def fail(request):
    return render(request, 'registration/password_reset_done_fail.html')




def send_email(request):
    subject = "message"
    to = ["limjs2671@gmail.com"]
    from_email = "basoup.t@gmail.com"
    message = "메지시 테스트"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()

def main(request):
    return render(request, 'main.html')

@login_required(login_url=URL_LOGIN)
def myinfo(request):
    return render(request, 'myinfo.html')

def find_id(request):
    return render(request, 'find_id.html')

def find_id_result(request):
    if request.method == "POST":
        find_email = request.POST.get('find_email', None)
        result = get_user_model().objects.filter(email = find_email).values_list('uid', flat=True)
        if result.exists():
            result = result
        else:
            result = 0
    return render(request, 'find_id_result.html', {'result':result})

def signup(request):
    if request.method == 'POST':
        phonenumber=request.POST['phonenumber']
        phonenumber=str(phonenumber)
        invest=request.POST['invest']


        if request.POST['password'] == request.POST['password1']:
            user = get_user_model().objects.create_user(
                                            uid=request.POST['uid'],
                                            password=request.POST['password'],
                                            username=request.POST['username'],
                                            gender=request.POST['gender'],
                                            job=request.POST['job'],
                                            email=request.POST['email'],
                                            phonenumber=phonenumber,
                                            invest=request.POST['invest'],
                                            invest_date=request.POST['invest_date'],
                                            u_chk=request.POST['u_chk'],
                                            pin=request.POST['pin'],
                                            birthday=request.POST['birthday'],
                                            )
            auth.login(request, user)
            return redirect('/')
        return render(request, 'signup.html')
    return render(request, 'signup.html')
class UserPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset.html' #템플릿을 변경하려면 이와같은 형식으로 입력

    def form_valid(self, form):
        if user.objects.filter(email=self.request.POST.get("email")).exists():
            opts = {
                'use_https': self.request.is_secure(),
                'token_generator': self.token_generator,
                'from_email': self.from_email,
                'email_template_name': self.email_template_name,
                'subject_template_name': self.subject_template_name,
                'request': self.request,
                'html_email_template_name': self.html_email_template_name,
                'extra_email_context': self.extra_email_context,
            }
            form.save(**opts)
            return super().form_valid(form)
        else:
            return render(self.request, 'registration/password_reset_done_fail.html')

class UserPasswordResetView(PasswordResetView):
    template_name = 'password_reset.form.html' #템플릿을 변경하려면 이와같은 형식으로 입력
    # success_url = reverse_lazy('password_reset_done')
    # form_class = PasswordResetForm

    def form_valid(self, form):
        if user.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'registration/password_reset_done_fail.html')

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html' #템플릿을 변경하려면 이와같은 형식으로 입력
