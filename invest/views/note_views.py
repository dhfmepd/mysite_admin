import json
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from ..forms import NoteForm
from ..models import Note
from interface.models import ResultData

@login_required(login_url='common:login')
def note_create_calendar(request):
    # 필수 파라미터
    record_date = request.GET.get('record_date', '')

    # YYYY-MM-DD 형식 포멧팅 처리
    display_date = datetime.strptime(record_date, '%Y-%m-%d')

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            # 작업일 기준 최신데이터 추출용 파라미터
            filter_date = datetime(display_date.year, display_date.month, display_date.day)
            if note.ticker:
                stock_data = ResultData.objects.filter(Q(func_name='stock_data_call') & Q(key_name=note.ticker) & Q(receipt_date__gte=filter_date)).first()
                if stock_data:
                    note.stock_data = stock_data.result_data
                else:
                    note.stock_data = None

            # JSON 형태 변환 저장
            note.author = request.user
            note.create_date = timezone.now()
            note.save()

            return redirect('invest:calendar')
    else:
        form = NoteForm()

    context = {'form': form, 'record_date': record_date, 'display_date': display_date}
    return render(request, 'invest/note_form.html', context)

@login_required(login_url='common:login')
def note_detail_calendar(request, note_id):
    # 조회
    note = get_object_or_404(Note, pk=note_id)
    record_date = note.record_date

    # YYYY-MM-DD 형식 포멧팅 처리
    display_date = datetime.strptime(record_date, '%Y-%m-%d')

    context = dict()

    if request.user != note.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('invest:calendar')

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            filter_date = datetime(display_date.year, display_date.month, display_date.day)
            if note.ticker:
                stock_data = ResultData.objects.filter(Q(func_name='stock_data_call') & Q(key_name=note.ticker) & Q(receipt_date__gte=filter_date)).first()
                if stock_data:
                    note.stock_data = stock_data.result_data
                else:
                    note.stock_data = None

            # JSON 형태 변환 저장
            note.author = request.user
            note.create_date = timezone.now()
            note.save()

            return redirect('invest:calendar')
    else:
        form = NoteForm(instance=note)

        if note.stock_data:
            stock_dict_data = json.loads(note.stock_data)
            stock_data = dict()

            stock_data['ticker'] = stock_dict_data.get('Ticker')
            stock_data['ticker_name'] = stock_dict_data.get('Ticker Name')
            stock_data['per'] = stock_dict_data.get('P/E')
            stock_data['forward_per'] = stock_dict_data.get('Forward P/E')
            stock_data['eps_ttm'] = stock_dict_data.get('EPS (ttm)')
            stock_data['market_cap'] = stock_dict_data.get('Market Cap')
            stock_data['earnings'] = stock_dict_data.get('Earnings')
            stock_data['eps_ttm'] = stock_dict_data.get('EPS (ttm)')
            stock_data['eps_next_yr'] = stock_dict_data.get('EPS next Y')

            stock_data['peg'] = stock_dict_data.get('PEG')
            stock_data['psr'] = stock_dict_data.get('P/S')
            stock_data['pbr'] = stock_dict_data.get('P/B')
            stock_data['roe'] = stock_dict_data.get('ROE')
            stock_data['gr_margin'] = stock_dict_data.get('Gross Margin')
            stock_data['op_margin'] = stock_dict_data.get('Oper.Margin')
            stock_data['pf_margin'] = stock_dict_data.get('Profit Margin')
            stock_data['roi'] = stock_dict_data.get('ROI')
            stock_data['short_float'] = stock_dict_data.get('Short Float')
            stock_data['rsi14'] = stock_dict_data.get('RSI(14)')
            stock_data['beta'] = stock_dict_data.get('Beta')
            stock_data['pt'] = stock_dict_data.get('Target Price')

            context['stock_data'] = stock_data

    context['form'] = form
    context['note'] = note
    context['record_date'] = record_date
    context['display_date'] = display_date

    return render(request, 'invest/note_form.html', context)