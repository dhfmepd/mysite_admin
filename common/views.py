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
    market_data = ResultData.objects.filter(Q(func_name='market_data_call')).order_by('-receipt_date').first()
    tsla_data = ResultData.objects.filter(Q(func_name='finviz_data_call') & Q(key_name='TSLA')).order_by('-receipt_date').first()

    market_json_data = json.loads(market_data.result_data)

    if not market_json_data.get('S&P 500'):
        snp500 = market_json_data.get('S&P Futures')
    else:
        snp500 = market_json_data.get('S&P 500')

    main_data = {
        'exch_rate_usd': json.loads(exch_data.result_data).get('Exch Rate'),
        'vix': market_json_data.get('Vix'),
        'bitcoin_usd': market_json_data.get('Bitcoin USD'),
        'snp500': snp500
    }

    return render(request, 'common/main.html', {'main_data': main_data})

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