import calendar
import json
from datetime import datetime
from dateutil.relativedelta import *
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import NoteForm
from ..models import Note

@login_required(login_url='common:login')
def calendar_main(request):
    # 초기값
    today = datetime.today()

    # 입력 파라미터
    year = request.GET.get('year', today.year)
    month = request.GET.get('month', today.month)
    mode = request.GET.get('mode', 'now')

    if mode == 'prev':
        today = datetime(int(year), int(month), 1) + relativedelta(months=-1)
        year = today.year
        month = today.month
    elif mode == 'next':
        today = datetime(int(year), int(month), 1) + relativedelta(months=1)
        year = today.year
        month = today.month

    # 새로 추가된 코드
    cal = calendar.monthcalendar(year, month)
    cal_data = []

    for week in cal:
        week_data = []
        for index, day in enumerate(week):
            color = "text-danger" if index == 6 else ""
            if day == 0:
                week_data.append((None, color, None))
            else:
                filter_date = str(year) + '-'

                if len(str(month)) == 1 :
                    filter_date = filter_date + '0' + str(month)
                else:
                    filter_date = filter_date + str(month)

                if len(str(day)) == 1:
                    filter_date = filter_date + '-0' + str(day)
                else:
                    filter_date = filter_date + '-' + str(day)

                note = Note.objects.filter(Q(record_date=filter_date))
                week_data.append((day, color, note))
        cal_data.append(week_data)

    result_data = {}  # 결과 데이터

    result_data['today'] = today
    result_data['month'] = str(month)
    result_data['month_text'] = today.strftime('%B')
    result_data['year'] = str(year)
    result_data['cal_data'] = cal_data

    return render(request, 'invest/calendar.html', result_data)

@login_required(login_url='common:login')
def note_create_calendar(request):
    record_date = request.GET.get('record_date', '')
    display_date = datetime.strptime(record_date, '%Y-%m-%d')

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            stock_data = dict()
            stock_data["State"] = request.POST.get("state")
            stock_data["Ticker"] = request.POST.get("ticker")
            stock_data["Price"] = request.POST.get("price")
            stock_data["Quantity"] = request.POST.get("quantity")

            note = form.save(commit=False)
            note.stock_data = json.dumps(stock_data)
            note.author = request.user
            note.create_date = timezone.now()
            note.save()
            return redirect('invest:calendar')
    else:
        form = NoteForm()

    context = {'form': form, 'record_date': record_date, 'display_date': display_date}
    return render(request, 'invest/note_form.html', context)