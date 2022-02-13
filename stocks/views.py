from django.shortcuts import render, redirect
# Create your views here.
import json
from django.http import HttpResponse,JsonResponse
from datetime import datetime
from django.db import transaction
from . import kocom
from . import stockcal as cal
from .models import *
from accounts import models as acc_models
from stocks.models import Stocksector
from django.db.models import Sum, Count, F
from decimal import *








def search_stock(request):
    wntlr = Stocksector.objects.all().values('ss_isusrtcd', 'ss_isukorabbrv')
    return render(request, 'search_stock.html', {'wntlr': wntlr})


def stock(request):
    stockheld = Stockheld.objects.filter(sh_userid=request.user.user_id)
    #print(stockheld)
    st2 = stockheld.values('sh_isusrtcd')
    st3 = Stockheld.objects.filter(sh_isusrtcd__in = st2).values('sh_share')
    #print(st3)

    stock_data = []
    stock_cal = cal.calculator()
    koscom_api = kocom.api()
    for element in stockheld:
        average_price = stock_cal.average_price(request.user.user_id, element.sh_isusrtcd)
        current_price = koscom_api.get_current_price(element.sh_marketcode, element.sh_isusrtcd)
        stock_data.append(
            [element.sh_isukorabbrv, average_price, current_price, element.sh_isusrtcd, element.sh_marketcode,element.sh_share])
        st1 = Stocktrading.objects.filter(st_isusrtcd = element.sh_isusrtcd).values('st_share')
        print(st1)

    return render(request, 'stock.html', {'stock_data': stock_data})


def portfolio(request):
    categorys =  Stockheld.objects.filter(sh_userid=request.user.user_id).values('sh_idxindmidclsscd','sh_isusrtcd').annotate(count=Count('sh_idxindmidclsscd')).order_by('-count')[:3]
    category_list = list(categorys.values('sh_idxindmidclsscd'))
    categorys_isurtcd = list(categorys.values('sh_isusrtcd'))
    category_keep = category_list[0:3]
    category_arr = []
    isurtcd_arr = []
    for i in category_keep:
        category_arr.append(i['sh_idxindmidclsscd'])
    for i in categorys_isurtcd:
        isurtcd_arr.append(i['sh_isusrtcd'])

    stock_suggestion1 = TotalMerge.objects.exclude(id__in = isurtcd_arr).filter(category__in =category_arr[0:3]).values("id",'per','pbr',"marketcode","name","category").annotate(
    ROA = (F('per') * Decimal('1.0') / F('pbr') * Decimal('1.0'))).order_by('-ROA')[0:5]
    stock_suggestion2 =list(stock_suggestion1)
    category_stock = []
    koscom_api = kocom.api()
    for element in stock_suggestion2:
        stock_suggestion = koscom_api.s_get_current_price(element['marketcode'],element['id'])
        category_stock.append([stock_suggestion,element['id'],element['per'],element['pbr'],element['marketcode'],element['name'],element['category']  ])

    result = {}
    stock_cal = cal.calculator()
    total_investment_amount = stock_cal.total_investment_amount(request.user.user_id)
    total_current_price = stock_cal.total_current_price(request.user.user_id)
    total_use_investment_amount = stock_cal.total_use_investment_amount(request.user.user_id)
    if total_investment_amount is False or total_current_price is False or total_use_investment_amount is False:
        result['total_investment_amount'] = 0
        result['total_current_price'] = 0
        result['total_use_investment_amount'] = 0
    else:

        result['category_stock'] = category_stock
        result['total_investment_amount'] = total_investment_amount
        result['total_current_price'] = total_current_price
        result['total_use_investment_amount'] = total_use_investment_amount
    return render(request, 'portfolio.html', result)

#
# def add_bookmark(request):
#     user_id =  request.user.user_id
#     if request.method == 'POST':
#         Bookmark =()
#         user_id = request.user.user_id,
#         marketcode = request.POST['marketcode'],
#         ss_isuSrtCd = request.POST['issuecode'],
#         activate = 1,
#         Bookmakr.save()
#         return redirect('/stock_info')
# def bookmark(request):
#     result_test = test.get('data' , None)
#     data = json.loads(request.body)
#     print(result_test)
#     if data:
#         bookmark.objects.create(
#             user_id =request.user.user_id,
#             marketcode = request.POST['marketcode'],
#             isuSrtCd = request.POST['issuecode'],
#             activate = 1
#         )
# def bookmark(request):
#     if request.method == 'POST':
#         marketcode = request.POST.get('marketcode', None) # ajax 통신을 통해서 template에서 POST방식으로 전달
#         issuecode = request.POST.get('issuecode', None) # ajax 통신을 통해서 template에서 POST방식으로 전달
#         mark = bookmark.objects.filter(user_id =request.user.user_id, marketcode=marketcode )
#         if mark:
#             ev = list(mark)
#         else:
#             ev = bookmark.objects.create(
#                 user_id =request.user.user_id,
#                 marketcode = marketcode,
#                 isuSrtCd = issuecode,
#                 activate = 1
#                 )
#             ev = list(ev)
#         print(ev)
#
#         data = {'ev': ev}
#         print(data)
#
#         return JsonResponse(data)

def boomark(request,isuSrtCd, marketcode ):
    isuSrtCd = str(isuSrtCd)
    marketcode= str(marketcode)
    print(type(marketcode))

    mark = bookmark.objects.filter(user_id =request.user.user_id, marketcode = marketcode, isuSrtCd = isuSrtCd)
    print(mark)
    if mark:
        mark.delete()
    else:
        bookmark.objects.create(
            user_id =request.user.user_id,
            marketcode = marketcode,
            isuSrtCd = issuecode,
            activate = 1
        )

    return redirect('/stock_info')




def stock_info(request):
    result = False
    koscom_api = kocom.api()
    stock_cal = cal.calculator()
    if request.method == 'POST':
        # marketcode = request.POST['marketcode']
        # print(marketcode)
        # ss_isuSrtCd = request.POST['issuecode']
# redirect( stock_info/marketcode/issuecode, )

        # mark = bookmark.objects.filter(user_id =request.user.user_id, marketcode = request.POST['marketcode'])
        # if mark:
        #     activate = 1
        # else:
        #     bookmark.objects.create(
        #         user_id =request.user.user_id,
        #         marketcode = request.POST['marketcode'],
        #         isuSrtCd = request.POST['issuecode'],
        #         activate = 1
        #     )

        result = koscom_api.get_stock_master(request.POST['marketcode'], request.POST['issuecode'])
        if result:
            result['curPrice'] = koscom_api.get_current_price(request.POST['marketcode'], request.POST['issuecode'])
            result['marketcode'] = request.POST['marketcode']
            result['total_allow_invest'] = request.user.invest - stock_cal.total_use_investment_amount(request.user.user_id)

            result['year_history'] = day_trdDd_matching(cal_year_history(koscom_api.get_stock_history(request.POST['marketcode'], request.POST['issuecode'],
                                                                                                      'M', '19800101', datetime.today().strftime('%Y%m%d'), 50)))
            result['month_history'] = day_trdDd_matching(koscom_api.get_stock_history(request.POST['marketcode'], request.POST['issuecode'],
                                                                                      'M', '19800101', datetime.today().strftime('%Y%m%d'), 50))
            result['week_history'] = day_trdDd_matching(koscom_api.get_stock_history(request.POST['marketcode'], request.POST['issuecode'],
                                                                                     'W', '19800101', datetime.today().strftime('%Y%m%d'), 50))
            result['day_history'] = day_trdDd_matching(koscom_api.get_stock_history(request.POST['marketcode'], request.POST['issuecode'],
                                                                                    'D', '19800101', datetime.today().strftime('%Y%m%d'), 50))
    return render(request, 'stock_info.html', {'result': result  })


def cal_year_history(history):
    try:
        temp_year = ''
        year_trdPrc = []
        for element in history:
            cur_year = str(element['trdDd'])[0:4]
            if cur_year != temp_year:
                temp_year = cur_year
                year_trdPrc.append(element)
        return year_trdPrc
    except Exception as e:
        print('Error in cal_year_history: \n', e)
        return False


def day_trdDd_matching(history):
    day_trdDd_array = []
    try:
        for element in history:
            day_trdDd_array.append({'trdDd': element['trdDd'], 'trdPrc': element['trdPrc']})
        return list(reversed(day_trdDd_array))
    except Exception as e:
        print('Error in day_trdDd_matching: \n', e)
        return False


def current_stock(request):
    data = json.loads(request.body)
    result = False
    if request.method == 'POST':
        result = kocom.api().get_current_stock(data['marketcode'], data['issuecode'])
    return JsonResponse({'result': result}, content_type='application/json')


def stock_search_result(request):
    data = json.loads(request.body)
    result = False
    if request.method == 'POST':
        try:
            stocksector = Stocksector.objects.filter(ss_isukorabbrv__icontains=data)
            result = []
            for elements in stocksector:
                result.append({
                    'logo': elements.ss_logo,
                    'isukorabbrv': elements.ss_isukorabbrv,
                    'issuecode': elements.ss_isusrtcd,
                    'marketcode': elements.ss_marketcode
                })
        except Exception as e:
            print('Error in stock_search_result: \n', e)
    return JsonResponse({'result': result}, content_type='application/json')


def buy_stock(request):
    data = json.loads(request.body)
    result = False
    if request.method == 'POST':
        total_rest_investment = cal.calculator().total_use_investment_amount(request.user.user_id)
        buy_price = int(data['share']) * int(data['current_price'])
        if (request.user.invest + total_rest_investment) - buy_price < 0:
            return JsonResponse({'result': '가상잔액이 부족합니다'}, content_type='application/json')

        stock_master = kocom.api().get_stock_master(data['marketcode'], data['issuecode'])
        stockheld_check = Stockheld.objects.filter(sh_userid=request.user.user_id,
                                                   sh_isusrtcd=stock_master['isuSrtCd']).exists()
        if stock_master and not stockheld_check:
            if stockheld_insert(request.user.user_id, data, stock_master):
                result = stocktrading_insert(request.user.user_id, data, stock_master, 'B')
        elif stock_master and stockheld_check:
            result = stocktrading_insert(request.user.user_id, data, stock_master, 'B')
        elif not stock_master and stockheld_check:
            result = False
        elif not stock_master and not stockheld_check:
            result = False
    return JsonResponse({'result': result}, content_type='application/json')


def sold_stock(request):
    data = json.loads(request.body)
    result = False
    if request.method == 'POST':
        get_share = cal.calculator().get_shares(request.user.user_id, data['issuecode'])
        sold_share = int(data['share'])
        if get_share - sold_share < 0:
            return JsonResponse({'result': '보유 주가 부족합니다'}, content_type='application/json')

        stock_master = kocom.api().get_stock_master(data['marketcode'], data['issuecode'])
        stockheld_check = Stockheld.objects.filter(sh_userid=request.user.user_id,
                                                   sh_isusrtcd=stock_master['isuSrtCd']).exists()
        if stock_master and stockheld_check:
            result = stocktrading_insert(request.user.user_id, data, stock_master, 'S')
    return JsonResponse({'result': result}, content_type='application/json')


def stockheld_insert(user_id, data, master):
    try:
        Stockheld(
            sh_userid=acc_models.user.objects.get(user_id=user_id),
            sh_isusrtcd=master['isuSrtCd'],
            sh_isucd=master['isuCd'],
            sh_isukorabbrv=master['isuKorAbbrv'],
            sh_marketcode=data['marketcode'],
            sh_idxindmidclsscd=master['idxIndMidclssCd']
        ).save()
        return True
    except Exception as e:
        print('Error in stockheld_insert: \n', e)
        return False


def stocktrading_insert(user_id, data, master, kind):
    try:
        if kind == 'B':
            data['current_price'] = -int(data['current_price'])
        print(transaction.savepoint())
        Stocktrading(
            st_userid=acc_models.user.objects.get(user_id=user_id),
            st_isusrtcd=master['isuSrtCd'],
            st_kind=kind,
            st_share=data['share'],
            st_price=data['current_price']
        ).save()
        stock_profit_input(user_id, int(data['current_price']))
        return True
    except Exception as e:
        print('Error in stocktrading_insert: \n', e)
        return False


def stock_profit_input(user_id, price):
    try:
        stockprofit_check = Stockprofit.objects.filter(sp_userid=user_id).exists()
        if not stockprofit_check:
            print(f'Insert: {user_id}, {price}')
            Stockprofit(
                sp_userid=user_id,
                sp_profit=price,
            ).save()
        else:
            print(f'Update: {user_id}, {price}')
            stockprofit_objects = Stockprofit.objects.get(sp_userid=user_id)
            stockprofit_objects.sp_userid = acc_models.user.objects.get(user_id=user_id)
            stockprofit_objects.sp_profit += price
            stockprofit_objects.save()
        return True
    except Exception as e:
        print('Error in stock_profit_input: \n', e)
        return False


def get_selectivemaster(request):
    data = json.loads(request.body)
    result = False
    if request.method == 'POST':
        result = kocom.api().get_selectivemaster(data['marketcode'], data['issuecode'])
    return JsonResponse({'result': result}, content_type='application/json')


def stocksector_update(request):
    if request.method == 'POST':
        stocksectors_bundle = kocom.api().get_stocksectors_bundle()
        if stocksectors_bundle:
            stocksector_insert(stocksectors_bundle)
            return JsonResponse({'result': 'Success'}, content_type='application/json')
        else:
            return JsonResponse({'result': 'Fail'}, content_type='application/json')


def stocksector_insert(stocksectors_bundle):
    print('==================> Start insert StockSector <==================')
    for stocksector in stocksectors_bundle:
        stockheld_check = Stocksector.objects.filter(ss_isusrtcd=stocksector['isusrtcd']).exists()
        if not stockheld_check:
            print('Insert: ', stocksector['isusrtcd'])
            Stocksector(
                ss_isusrtcd=stocksector['isusrtcd'],
                ss_isukorabbrv=stocksector['isukorabbrv'],
                ss_marketcode=stocksector['marketcode'],
                ss_idxindmidclsscd=stocksector['idxindmidclsscd'],
                ss_haltyn=stocksector['haltyn'],
            ).save()
        else:
            print('Update: ', stocksector['isusrtcd'])
            stocksector_objects = Stocksector.objects.get(ss_isusrtcd=stocksector['isusrtcd'])
            stocksector_objects.ss_isusrtcd = stocksector['isusrtcd']
            stocksector_objects.ss_isukorabbrv = stocksector['isukorabbrv']
            stocksector_objects.ss_marketcode = stocksector['marketcode']
            stocksector_objects.ss_idxindmidclsscd = stocksector['idxindmidclsscd']
            stocksector_objects.ss_haltyn = stocksector['haltyn']
            stocksector_objects.save()


def get_history(request):
    data = json.loads(request.body)
    result = False
    if request.method == 'POST':
        result = kocom.api().get_stock_history(data['marketcode'], data['issuecode'],
                                               data['trnsmCycleTpCd'], data['inqStrtDd'],
                                               data['inqEndDd'], data['reqCnt'])
    return JsonResponse({'result': result}, content_type='application/json')

def top2(request):
    categorys =  Stockheld.objects.filter(sh_userid=request.user.user_id).values('sh_idxindmidclsscd','sh_isusrtcd').annotate(count=Count('sh_idxindmidclsscd')).order_by('-count')[:3]
    category_list = list(categorys.values('sh_idxindmidclsscd'))
    categorys_isurtcd = list(categorys.values('sh_isusrtcd'))
    category_keep = category_list[0:3]
    category_arr = []
    isurtcd_arr = []
    for i in category_keep:
        category_arr.append(i['sh_idxindmidclsscd'])
    for i in categorys_isurtcd:
        isurtcd_arr.append(i['sh_isusrtcd'])

    stock_suggestion1 = TotalMerge.objects.exclude(id__in = isurtcd_arr).filter(category__in =category_arr[0:3]).values("id",'per','pbr',"marketcode","name","category").annotate(
    ROA = (F('per') * Decimal('1.0') / F('pbr') * Decimal('1.0'))).order_by('-ROA')[0:5]
    stock_suggestion2 =list(stock_suggestion1)

    category_stock = []
    koscom_api = kocom.api()
    for element in stock_suggestion2:
        stock_suggestion = koscom_api.s_get_current_price(element['marketcode'],element['id'])
        category_stock.append([stock_suggestion,element['id'],element['per'],element['pbr'],element['marketcode'],element['name'],element['category']  ])
        print(category_stock)
    return render(request, 'top2.html', {'category_stock': category_stock})
