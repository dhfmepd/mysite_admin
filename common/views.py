import json
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from common.forms import UserForm
from interface.models import ResultData
from .models import Code

def index(request):
    """
    Main Page 출력
    """
    if request.user.is_authenticated == True:
        return redirect('common:main')

    return redirect('common:login')

@login_required(login_url='common:login')
def main(request):
    """
    Dashboard 출력
    """
    symbol = request.GET.get('symbol', '')  # 페이지
    anchor = "stock_area"

    ticker_list = Code.objects.filter(Q(group_code='TICKER')).order_by('detail_code')

    if not symbol:
        symbol = ticker_list[0].detail_code
        anchor = ""

    stock_data = ResultData.objects.filter(Q(func_name='stock_data_call') & Q(key_name=symbol)).order_by('-receipt_date').first()
    exch_data = ResultData.objects.filter(Q(func_name='exch_data_call') & Q(key_name='KRW2USD')).order_by('-receipt_date').first()
    index_data = ResultData.objects.filter(Q(func_name='index_data_call')).order_by('-receipt_date').first()
    crypto_data = ResultData.objects.filter(Q(func_name='crypto_data_call')).order_by('-receipt_date').first()
    tech_data = ResultData.objects.filter(Q(func_name='tech_data_call')).order_by('-receipt_date').first()
    hist_data = ResultData.objects.filter(Q(func_name='stock_hist_data_call') & Q(key_name=symbol)).order_by('-receipt_date').first()
    earn_data = ResultData.objects.filter(Q(func_name='stock_earning_data_call') & Q(key_name=symbol)).order_by('-receipt_date').first()

    stock_dict_data = json.loads(stock_data.result_data)
    exch_json_data = json.loads(exch_data.result_data)
    index_json_data = json.loads(index_data.result_data)
    crypto_json_data = json.loads(crypto_data.result_data)
    tech_list = json.loads(tech_data.result_data).get('tech_list')
    hist_list = json.loads(hist_data.result_data).get('hist_list')
    earn_label_list = json.loads(earn_data.result_data).get('label_list')
    earn_act_data_list = json.loads(earn_data.result_data).get('act_data_list')
    earn_est_data_list = json.loads(earn_data.result_data).get('est_data_list')

    hist_label_list = list()
    hist_data_list = list()

    for index, hist_data in enumerate(hist_list):
        hist_label_list.append(hist_data.get('date'))
        hist_data_list.append(hist_data.get('price'))

    hist_label_list.reverse()
    hist_data_list.reverse()

    main_data = dict()

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
    main_data['gr_margin'] = stock_dict_data.get('Gross Margin')
    main_data['op_margin'] = stock_dict_data.get('Oper.Margin')
    main_data['pf_margin'] = stock_dict_data.get('Profit Margin')
    main_data['roi'] = stock_dict_data.get('ROI')
    main_data['short_float'] = stock_dict_data.get('Short Float')
    main_data['rsi14'] = stock_dict_data.get('RSI(14)')
    main_data['beta'] = stock_dict_data.get('Beta')
    main_data['pt'] = stock_dict_data.get('Target Price')


    main_data['exch_rate'] = exch_json_data.get('Exch Rate')
    main_data['exch_rate_change'] = exch_json_data.get('Exch Rate Change')
    main_data['exch_rate_change_percent'] = exch_json_data.get('Exch Rate Change Percent')
    main_data['exch_rate_color'] = colorSelection(exch_json_data.get('Exch Rate Change'))
    main_data['snp500'] = index_json_data.get('S&P 500')
    main_data['snp500_change'] = index_json_data.get('S&P 500 Change')
    main_data['snp500_change_percent'] = index_json_data.get('S&P 500 Change Percent')
    main_data['snp500_color'] = colorSelection(index_json_data.get('S&P 500 Change'))
    main_data['nasdaq'] = index_json_data.get('NASDAQ Composite')
    main_data['nasdaq_change'] = index_json_data.get('NASDAQ Composite Change')
    main_data['nasdaq_change_percent'] = index_json_data.get('NASDAQ Composite Change Percent')
    main_data['nasdaq_color'] = colorSelection(index_json_data.get('NASDAQ Composite Change'))
    main_data['bitcoin'] = crypto_json_data.get('Bitcoin USD')
    main_data['bitcoin_change'] = crypto_json_data.get('Bitcoin USD Change')
    main_data['bitcoin_change_percent'] = crypto_json_data.get('Bitcoin USD Change Percent')
    main_data['bitcoin_color'] = colorSelection(crypto_json_data.get('Bitcoin USD Change'))

    return render(request, 'common/main.html', {'anchor': anchor, 'symbol': symbol, 'ticker_list': ticker_list, 'main_data': main_data, 'tech_list': tech_list, 'hist_label_list': hist_label_list, 'hist_data_list': hist_data_list, 'earn_label_list': earn_label_list, 'earn_act_data_list': earn_act_data_list, 'earn_est_data_list': earn_est_data_list})

def colorSelection(data):
    if data[0:1] == '+':
        return 'success'
    elif data[0:1] == '-':
        return 'danger'
    else:
        return 'dark'

def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'common/index.html')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

def page_not_found(request, exception):
    """
    404 Page not found
    """
    print('=========================404=========================')
    return render(request, 'common/404.html', {})