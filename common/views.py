import json
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from common.forms import UserForm
from interface.models import ResultData

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
    exch_data = ResultData.objects.filter(Q(func_name='exch_data_call') & Q(key_name='KRW2USD')).order_by('-receipt_date').first()
    index_data = ResultData.objects.filter(Q(func_name='index_data_call')).order_by('-receipt_date').first()
    crypto_data = ResultData.objects.filter(Q(func_name='crypto_data_call')).order_by('-receipt_date').first()
    tech_data = ResultData.objects.filter(Q(func_name='tech_data_call')).order_by('-receipt_date').first()

    exch_json_data = json.loads(exch_data.result_data)
    index_json_data = json.loads(index_data.result_data)
    crypto_json_data = json.loads(crypto_data.result_data)
    tech_list = json.loads(tech_data.result_data).get('tech_list')

    main_data = dict()

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

    return render(request, 'common/main.html', {'main_data': main_data, 'tech_list': tech_list})

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