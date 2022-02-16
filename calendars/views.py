from mysettings import ALIGO_SECRET_KEY, ALIGO_USERID, ALIGO_SENDER
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import auth, messages
from django.core import serializers
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from accounts.models import user
from .models import Income, Spend, Stocksector, AccountBook
from django.contrib.auth.decorators import login_required
from .calendarsforms import SpendForm, IncomeForm
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date
import datetime, requests
from django.db.models import Sum, Count
import os, json
from django.conf import settings
from django.views.generic import View
from django.contrib.auth.hashers import check_password
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from stocks import stockcal as cal
from stocks import kocom
from stocks.models import Stocksector

# Create your views here.
URL_LOGIN = '/login'


@login_required(login_url=URL_LOGIN)
def home(request):
    if request.method == 'POST':
        user = request.user.user_id
        phonenumber = request.POST.get('phonenumber', None)
        phonenumber = str(phonenumber)
        invest = request.POST['invest']
        birthday = request.POST['birthday']
        pin = request.POST['pin']
        
        if invest == '0':
            #invest_date = None
            invest_date = date(1111,1,11)
        else:
            invest_date = datetime.now()
        
        if birthday == '':
            #birthday = date(1111, 1, 11)
            birthday = datetime.now()
        else:
            birthday = birthday

        if pin == '':
            pin = '0000'
        else:
            pin = pin
        
        user = get_user_model().objects.filter(user_id=user).update(
            u_chk=request.POST['u_chk'],
            username=request.POST['username'],
            gender=request.POST.get("gender"),
            job=request.POST.get("job"),
            phonenumber=phonenumber,
            birthday=birthday,
            pin=pin,
            invest=invest,
        )
        print("저장후 폰넘버", phonenumber)
        return redirect('/')
    invest = request.user.invest
    user = request.user.user_id
    now = datetime.datetime.now()
    month = now.strftime('%m').replace('0', '')
    year = now.strftime('%Y')
    # 월별 기간 필터링
    spend_month_filter2 = Spend.objects.filter(user_id=user, spend_date__month=month).values('spend_id', 'kind',
                                                                                             'spend_date', 'amount',
                                                                                             'place', 'category')
    income_month_filter2 = Income.objects.filter(user_id=user, income_date__month=month).values('income_id', 'kind',
                                                                                                'income_date', 'amount',
                                                                                                'income_way',
                                                                                                'income_way')
    # 월 총 수입, 지출
    spend_sum = spend_month_filter2.values('amount').aggregate(Sum('amount'))
    spend_sum_value = list(spend_sum.values())
    income_sum = income_month_filter2.values('amount').aggregate(Sum('amount'))
    income_sum_value = list(income_sum.values())
    stock_cal = cal.calculator()
    total_investment_amount = stock_cal.total_investment_amount(request.user.user_id)
    total_use_investment_amount = stock_cal.total_use_investment_amount(request.user.user_id)
    #son = total_current_price + total_use_investment_amount
    total_current_price = stock_cal.total_current_price(request.user.user_id)
    if total_current_price is None:
        total_current_price = 0
    else:
        total_current_price = total_current_price
    son = total_current_price + total_use_investment_amount
    print(total_current_price)
    home_chartjs_data = [invest, son]
    print( home_chartjs_data)
    for spend_sum_value in spend_sum_value:
        if spend_sum_value == None:
            home_chartjs_data.append(0)
        else:
            home_chartjs_data.append(spend_sum_value)
    for income_sum_value in income_sum_value:
        if income_sum_value == None:
            home_chartjs_data.append(0)
        else:
            home_chartjs_data.append(income_sum_value)
    return render(request, 'home.html', {'month': month, 'Expenditure': spend_sum, 'Income': income_sum, 'income_sum_value':income_sum_value,
                                         'Home_chartjs_data': home_chartjs_data, 'Total_investment_amount':total_investment_amount, 'son':son})


def recom(request):
    return render(request, 'recom.html')


def summary(request):
    user = request.user.user_id
    now = datetime.datetime.now()
    month = now.strftime('%m')
    year = now.strftime('%Y')
    # 월별 기간 필터링
    spend_month_filter2 = Spend.objects.filter(user_id=user, spend_date__month=month).values('spend_id', 'kind',
                                                                                             'spend_date', 'amount',
                                                                                             'place', 'category')
    income_month_filter2 = Income.objects.filter(user_id=user, income_date__month=month).values('income_id', 'kind',
                                                                                                'income_date', 'amount',
                                                                                                'income_way',
                                                                                                'income_way')
    spend_month_filter = Spend.objects.filter(user_id=user).values('spend_id', 'kind', 'spend_date', 'amount', 'place',
                                                                   'category')
    income_month_filter = Income.objects.filter(user_id=user).values('income_id', 'kind', 'income_date', 'amount',
                                                                     'income_way', 'income_way')

    # 월별 쿼리셋 합치기
    detail_month = spend_month_filter.union(income_month_filter).order_by('-spend_date')

    spend_day_sum2 = spend_month_filter.values('spend_date__day', 'kind').annotate(amount=Sum('amount')).order_by(
        '-spend_date__day').values('spend_date', 'kind', 'amount')
    income_day_sum2 = income_month_filter.values('income_date__day', 'kind').annotate(amount=Sum('amount')).order_by(
        '-income_date__day').values('income_date', 'kind', 'amount')
    # spend_day_sum = spend_month_filter.values('spend_date__day').annotate(amount=Sum('amount')).order_by('-spend_date__day')
    # income_day_sum = income_month_filter.values('income_date__day').annotate(amount=Sum('amount')).order_by('-income_date__day')

    detail_day = income_day_sum2.union(spend_day_sum2)

    # 월 총 수입, 지출
    spend_sum = spend_month_filter2.aggregate(Sum('amount'))
    income_sum = income_month_filter2.aggregate(Sum('amount'))

    return render(request, 'summary.html', {
        'Spend_day': spend_day_sum2,
        'Income_day': income_day_sum2,
        'Detail_month': detail_month,
        'detail_day': detail_day,
        'Expenditure': spend_sum,
        'Income': income_sum,

        'month': month,
        'spend_day_sum2': spend_day_sum2,
        'income_day_sum2': income_day_sum2,

    })


def history(request):
    input_year = request.POST.get('input_year', None)
    input_month = request.POST.get("input_month", None)
    user = request.user.user_id
    now = datetime.datetime.now()
    if input_year:
        year = input_year
    if input_month:
        month = input_month
    else:
        month = now.strftime('%m')
        year = now.strftime('%Y')

    # 월별 기간 필터링
    spend_month_filter = Spend.objects.filter(user_id=user, spend_date__year=year, spend_date__month=month).values('spend_id', 'kind',
                                                                                            'spend_date', 'amount',
                                                                                            'place', 'category')
    income_month_filter = Income.objects.filter(user_id=user, income_date__year=year, income_date__month=month).values('income_id', 'kind',
                                                                                               'income_date', 'amount',
                                                                                               'income_way',
                                                                                               'income_way')
    # 월 총 수입, 지출
    spend_sum = spend_month_filter.aggregate(Sum('amount'))
    income_sum = income_month_filter.aggregate(Sum('amount'))
    # 월별 쿼리셋 합치기
    detail_month = spend_month_filter.union(income_month_filter).order_by('-spend_date')

    spend_day_sum = spend_month_filter.values('spend_date__day').annotate(amount=Sum('amount')).order_by(
        '-spend_date__day')
    income_day_sum = income_month_filter.values('income_date__day').annotate(amount=Sum('amount')).order_by(
        '-income_date__day')

    # detail_day = income_day_sum.union(spend_day_sum)

    return render(request, 'history.html',
                  {'year': year,
                   'month': month,
                   'Spend_day': spend_day_sum,
                   'Income_day': income_day_sum,
                   'Detail_month': detail_month,
                   # 'detail_day':detail_day,
                   'Expenditure': spend_sum,
                   'Income': income_sum,
                   })


@login_required(login_url=URL_LOGIN)
def top5(request):
    user = request.user.user_id
    now = datetime.datetime.now()
    month = now.strftime('%m')
    year = now.strftime('%Y')
    # 월별 기간 필터링
    spend_month_filter = Spend.objects.filter(user_id=user, spend_date__month=month).values('spend_id', 'kind',
                                                                                            'spend_date', 'amount',
                                                                                            'place', 'category')
    income_month_filter = Income.objects.filter(user_id=user, income_date__month=month).values('income_id', 'kind',
                                                                                               'income_date', 'amount',
                                                                                               'income_way',
                                                                                               'income_way')
    # 소비 TOP5 카테고리 , 카드, 거래처
    category_amount = spend_month_filter.values('category', 'card', 'place').annotate(amount=Sum('amount')).order_by(
        '-amount')[:5]

    # 소비 TOP5 카테고리 금액 합계
    category_sum = spend_month_filter.values('category').annotate(amount=Sum('amount')).order_by('-amount')[:5]
    category_card = spend_month_filter.values('card').annotate(amount=Sum('amount')).order_by('-amount')[:5]
    category_place = spend_month_filter.values('place').annotate(amount=Sum('amount')).order_by('-amount')[:5]

    category_category = spend_month_filter.values('category').annotate(amount=Sum('amount')).order_by('-amount')[:5]

    # 요약 페이지_카테고리 건수별 TOP5
    category_amount_count = spend_month_filter.values('category').annotate(count=Count('category')).order_by('-count')[:5]

    category_stock = []
    koscom_api = kocom.api()
    for element in category_place:
        find_market_code = Stocksector.objects.filter(ss_isukorabbrv=element['place']).values_list('ss_marketcode', flat=True)
        find_market_code1 = Stocksector.objects.filter(ss_isukorabbrv=element['place']).values_list('ss_isusrtcd', flat=True)

        find_market_code = list(find_market_code)
        find_market_code1 = list(find_market_code1)
        market_code = find_market_code[0] if find_market_code else None
        issuecode = find_market_code1[0] if find_market_code1 else None
        current_price = koscom_api.get_current_price(market_code , issuecode  )
        print(current_price)
        category_stock.append([current_price, element['amount'], element['place'], issuecode, market_code])
        print(category_stock)

    category_amount_data = []
    category_amount_label = []
    category_count_data = []
    category_count_label = []
    for item in category_amount:
        category_amount_data.append(item['amount'])
        category_amount_label.append(item['category'])
    for item in category_amount_count:
        category_count_data.append(item['count'])
        category_count_label.append(item['category'])

    return render(request, 'top5.html',
                  {'month': month,
                   'Category_amount_data': category_amount_data,
                   'Category_amount_labels': category_amount_label,
                   'Category_count_data': category_count_data,
                   'Category_count_label': category_count_label,
                   'Category_count': category_amount_count,
                   'Category_sum': category_sum,
                   'category_card': category_card,
                   'category_place': category_place,
                   'category_stock':category_stock})


def category_detail(request, int):
    now = datetime.datetime.now()
    user = request.user.user_id
    three_months_ago = now - relativedelta(months=1)
    category = Spend.objects.filter(user_id=user, category=int, spend_date__range=(three_months_ago, now)).order_by(
        'spend_date')
    print('categorycategorycategorycategory--->', str(category))

    return render(request, 'category_detail.html', {'category': category, 'int': int})


def detail_search(request):
    user = request.user.user_id
    start_date = request.POST.get('start_date', None )
    end_date = request.POST.get("end_date", None)
    spend_date = Spend.objects.filter(user_id=user, spend_date__range=(start_date, end_date)).values('spend_id', 'kind',
                                                                                                     'spend_date',
                                                                                                     'amount', 'place',
                                                                                                     'category')
    income_date = Income.objects.filter(user_id=user, income_date__range=(start_date, end_date)).values('income_id',
                                                                                                        'kind',
                                                                                                        'income_date',
                                                                                                        'amount',
                                                                                                        'income_way',
                                                                                                        'income_way')
    total_date = spend_date.union(income_date).order_by('-spend_date')
    return render(request, 'detail_search.html', {'total_date': total_date,'start_date':start_date, 'end_date':end_date})


# 알리고 관련 기능
@csrf_exempt
def ajax_sendSMS(request):
    if request.method == "POST":
        NUM = request.POST.get("NUM", None)
        KEY = request.POST.get("KEY", None)
        print(str(NUM) + '그리고' + str(KEY))

    send_url = 'https://apis.aligo.in/send/'  # 요청을 던지는 URL, 현재는 문자보내기
    # ================================================================== 문자 보낼 때 필수 key값
    # API key, userid, sender, receiver, msg
    # API키, 알리고 사이트 아이디, 발신번호, 수신번호, 문자내용
    sms_data = {
        'key': ALIGO_SECRET_KEY,  # api key
        'userid': ALIGO_USERID,  # 알리고 사이트 아이디
        'sender': ALIGO_SENDER,  # 발신번호
        'receiver': NUM,  # 수신번호 (,활용하여 1000명까지 추가 가능)
        'msg': f'[LEMON]인증번호 [{KEY}]를 입력해주세요.',  # 문자 내용
        'testmode_yn': 'Y'  # 테스트모드 적용 여부 Y/N
        # 'msg_type' : 'SMS', #메세지 타입 (SMS, LMS)
        # 'title' : 'testTitle', #메세지 제목 (장문에 적용)
        # 'destination' : '01000000000|고객명', # %고객명% 치환용 입력
        # 'rdate' : '예약날짜',
        # 'rtime' : '예약시간',
    }
    requests.post(send_url, data=sms_data)
    data = {}

    return JsonResponse(data, safe=False)


def add_income_calendar(request):
    if request.method == "POST":
        iform = IncomeForm(request.POST)
        if iform.is_valid():
            user_id = request.POST['user'],
            kind = iform.cleaned_data['kind'],
            amount = iform.cleaned_data['amount'],
            income_date = iform.cleaned_data['income_date'],
            income_way = iform.cleaned_data['income_way'],
            memo = iform.cleaned_data['memo']
            iform.save()
            return redirect('/history')
    else:
        iform = IncomeForm()
    wntlr = Stocksector.objects.all().values('ss_isusrtcd', 'ss_isukorabbrv')
    return render(request, 'add_income_calendar.html', {'wntlr': wntlr})


def add_spend_calendar(request):
    if request.method == "POST":
        sform = SpendForm(request.POST)
        if sform.is_valid():
            user_id = request.POST['user'],
            kind = sform.cleaned_data['kind'],
            amount = sform.cleaned_data['amount'],
            place = sform.cleaned_data['place'],
            spend_date = sform.cleaned_data['spend_date'],
            way = sform.cleaned_data['way'],
            category = sform.cleaned_data['category'],
            card = sform.cleaned_data['card'],
            memo = sform.cleaned_data['memo'],
            #stock = sform.cleaned_data['stock']
            sform.save()
            return redirect('/history')
    else:
        sform = SpendForm()
    wntlr = Stocksector.objects.all().values('ss_isusrtcd', 'ss_isukorabbrv')
    return render(request, 'add_spend_calendar.html', {'wntlr': wntlr})

# SMS문자내역 입력
def sms_add_spend_calendar(request, date, amount, place):
    if request.method == "POST":
        date = request.POST.get("date", None)
        amount = request.POST.get("amount", None)
        place = request.POST.get("place", None)
        wntlr = Stocksector.objects.all().values('ss_isusrtcd', 'ss_isukorabbrv')

    return render(request, 'sms_add_spend_calendar.html', {'date': date, 'amount': amount, 'place': place, 'wntlr': wntlr})

def edit_calendar(request, spend_id, kind):
    user = request.user.user_id
    if kind == '지출':
        spe = Spend.objects.filter(spend_id=spend_id, user_id=user)
        wntlr = Stocksector.objects.all().values('ss_isusrtcd', 'ss_isukorabbrv')
        return render(request, 'sedit_calendar.html', {'spe': spe, 'wntlr': wntlr})
    if kind == "수입":
        income = Income.objects.filter(income_id=spend_id, user_id=user)
        return render(request, 'iedit_calendar.html', {'income': income})


def sedit_calendar(request, spend_id):
    if request.method == "POST":
        user = request.user.user_id
        # if place == stock:
        #     stock = 000000
        spe = Spend.objects.filter(spend_id=spend_id, user_id=user).update(
            amount=request.POST['amount'],
            place=request.POST['place'],
            spend_date=request.POST['spend_date'],
            way=request.POST['way'],
            category=request.POST['category'],
            card=request.POST['card'],
            memo=request.POST['memo'],
            )
        return redirect('/history')


def iedit_calendar(request, income_id):
    if request.method == "POST":
        user = request.user.user_id
        spe = Income.objects.filter(income_id=income_id, user_id=user).update(
            kind=request.POST['kind'],
            amount=request.POST['amount'],
            income_date=request.POST['income_date'],
            income_way=request.POST['income_way'],
            memo=request.POST['memo'], )
        return redirect('/history')

def delete_shistory(request, spend_id):
    spend = Spend.objects.get(spend_id = spend_id)
    spend.delete()
    return redirect('/history')

def delete_ihistory(request, income_id):
    income = Income.objects.get(income_id = income_id)
    income.delete()
    return redirect('/history')

@csrf_exempt
def ajax_pushdate(request):
    if request.method == "POST":
        user = request.user.user_id
        date = request.POST.get("clikDate", None)
        spend = Spend.objects.filter(user_id=user, spend_date=date).values('spend_id','kind', 'spend_date', 'amount', 'place')
        income = Income.objects.filter(user_id=user, income_date=date).values('income_id','kind', 'income_date', 'amount',
                                                                              'income_way')
        detail_month = income.union(spend).order_by('kind')
        even1 = list(detail_month.values('income_id','kind', 'income_date', 'amount', 'income_way'))
        evens = {'msg1': even1}

        return JsonResponse(evens)
