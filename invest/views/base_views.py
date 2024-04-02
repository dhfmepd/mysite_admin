import json
import calendar
from datetime import datetime
from dateutil.relativedelta import *
from django.db.models import Q, F
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags.humanize import ordinal
from common.models import Code
from interface.models import ResultData
from ..models import Note

@login_required(login_url='common:login')
def calendar_main(request):
    # 초기값
    today = datetime.today()

    # 입력 파라미터
    year = request.GET.get('year', today.year)
    month = request.GET.get('month', today.month)
    mode = request.GET.get('mode', 'now')
    tgt_type = request.GET.get('tgt_type', '')
    tgt_day = request.GET.get('tgt_day', '')

    cur_day = datetime(int(year), int(month), 1)

    if mode == 'prev':
        cur_day = cur_day + relativedelta(months=-1)
        year = cur_day.year
        month = cur_day.month
    elif mode == 'next':
        cur_day = cur_day + relativedelta(months=1)
        year = cur_day.year
        month = cur_day.month

    # 새로 추가된 코드
    cal = calendar.monthcalendar(int(year), int(month))
    cal_data = []

    for week in cal:
        week_data = []
        for index, day in enumerate(week):
            color = ""


            if index == 5:
                # Saturday 폰트 컬러 처리 (파란색)
                color = "font-weight-bold text-primary"
            elif index == 6:
                # Sunday 폰트 컬러 처리 (붉은색)
                color = "font-weight-bold text-danger"

            if day == 0:
                week_data.append((None, color, None, None))
            else:
                filter_date = convertDateInputFormat(year, month, day)
                # 일자 별 Note Counting 표시용 조회
                memo_note = Note.objects.filter(Q(record_date=filter_date) & Q(type="MM"))
                trade_note = Note.objects.filter(Q(record_date=filter_date) & Q(type="TD"))
                week_data.append((day, color, memo_note, trade_note))
        cal_data.append(week_data)

    result_data = {}  # 결과 데이터

    result_data['today'] = today
    result_data['cur_day'] = cur_day
    result_data['month'] = str(month)
    result_data['month_text'] = cur_day.strftime('%B')
    result_data['year'] = str(year)
    
    # 하단 조회결과 타이르 처리
    tgt_header_text = tgt_type
    for code, label in Note.type_choices:
        if code == tgt_type:
            tgt_header_text = label + " - " + ordinal(int(tgt_day))

    result_data['tgt_type'] = tgt_type
    result_data['tgt_header_text'] = tgt_header_text
    result_data['cal_data'] = cal_data
    
    # 게시물 카운트 클릭 케이스(조건 : Target Day, Target Type)
    if tgt_day:
        tgt_date = convertDateInputFormat(year, month, tgt_day)
        note_list = Note.objects.filter(Q(record_date=tgt_date) & Q(type=tgt_type)).annotate(row_number=Window(expression=RowNumber(), order_by=F('id').asc())).order_by("-id")
        result_data['note_list'] = note_list
        result_data['anchor'] = 'note_table'

    return render(request, 'invest/calendar.html', result_data)

def ordinal(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

def convertDateInputFormat(year, month, day):
    date = str(year) + '-'
    if len(str(month)) == 1:
        date = date + '0' + str(month)
    else:
        date = date + str(month)

    if len(str(day)) == 1:
        date = date + '-0' + str(day)
    else:
        date = date + '-' + str(day)

    return date


@login_required(login_url='common:login')
def stock_detail(request):
    symbol = request.GET.get('symbol', '')  # 페이지
    ticker_list = Code.objects.filter(Q(group_code='TICKER')).order_by('detail_code_name')

    if not symbol:
        symbol = ticker_list[0].detail_code

    context = dict()

    context['symbol'] = symbol
    context['ticker_list'] = ticker_list

    stock_data = ResultData.objects.filter(Q(func_name='stock_data_call') & Q(key_name=symbol)).order_by('-receipt_date').first()
    hist_data = ResultData.objects.filter(Q(func_name='stock_hist_data_call') & Q(key_name=symbol)).order_by('-receipt_date').first()
    earn_data = ResultData.objects.filter(Q(func_name='stock_earning_data_call') & Q(key_name=symbol)).order_by('-receipt_date').first()

    main_data = dict()

    if stock_data:
        stock_dict_data = json.loads(stock_data.result_data)

        main_data['price'] = stock_dict_data.get('Price')
        main_data['change'] = stock_dict_data.get('Change')

        main_data['ticker'] = stock_dict_data.get('Ticker')
        main_data['ticker_name'] = stock_dict_data.get('Ticker Name')
        main_data['per'] = stock_dict_data.get('P/E')
        main_data['forward_per'] = stock_dict_data.get('Forward P/E')
        main_data['eps_ttm'] = stock_dict_data.get('EPS (ttm)')
        main_data['market_cap'] = stock_dict_data.get('Market Cap')
        main_data['earnings'] = stock_dict_data.get('Earnings')
        main_data['eps_ttm'] = stock_dict_data.get('EPS (ttm)')
        main_data['eps_next_yr'] = stock_dict_data.get('EPS next Y')

        main_data['peg'] = stock_dict_data.get('PEG')
        main_data['psr'] = stock_dict_data.get('P/S')
        main_data['pbr'] = stock_dict_data.get('P/B')
        main_data['roe'] = stock_dict_data.get('ROE')
        main_data['eps_yoy_ttm'] = stock_dict_data.get('EPS Y/Y TTM')
        main_data['sale_yoy_ttm'] = stock_dict_data.get('Sales Y/Y TTM')
        main_data['eps_qoq'] = stock_dict_data.get('EPS Q/Q')
        main_data['sale_qoq'] = stock_dict_data.get('Sales Q/Q')
        main_data['short_float'] = stock_dict_data.get('Short Float')
        main_data['rsi14'] = stock_dict_data.get('RSI (14)')
        main_data['beta'] = stock_dict_data.get('Beta')
        main_data['pt'] = stock_dict_data.get('Target Price')

        rating_list = stock_dict_data.get('Rating List')

        for idx, rating_data in enumerate(rating_list):
            rating_data['no'] = idx+1
            rating_data['date'] = rating_data.get("Date")
            rating_data['action'] = rating_data.get("Action")
            rating_data['analyst'] = rating_data.get("Analyst")
            rating_data['rating_change'] = rating_data.get("Rating Change")
            rating_data['price_target_change'] = rating_data.get("Price Target Change")

        context['main_data'] = main_data
        context['rating_list'] = rating_list

    hist_label_list = list()
    hist_data_list = list()

    if hist_data:
        hist_list = json.loads(hist_data.result_data).get('hist_list')

        for hist_data in hist_list:
            hist_label_list.append(hist_data.get('date'))
            hist_data_list.append(hist_data.get('price'))

        hist_label_list.reverse()
        hist_data_list.reverse()

    context['hist_label_list'] = hist_label_list
    context['hist_data_list'] = hist_data_list

    if earn_data:
        earn_label_list = json.loads(earn_data.result_data).get('label_list')
        earn_act_data_list = json.loads(earn_data.result_data).get('act_data_list')
        earn_est_data_list = json.loads(earn_data.result_data).get('est_data_list')

        context['earn_label_list'] = earn_label_list
        context['earn_act_data_list'] = earn_act_data_list
        context['earn_est_data_list'] = earn_est_data_list
    else:
        context['earn_label_list'] = list()
        context['earn_act_data_list'] = list()
        context['earn_est_data_list'] = list()

    return render(request, 'invest/stock_detail.html', context)