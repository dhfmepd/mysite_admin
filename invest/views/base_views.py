import calendar
from datetime import datetime
from dateutil.relativedelta import *
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import NoteForm

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
                week_data.append((None, color))
            else:
                #count = 1  #
                week_data.append((day, color))
        cal_data.append(week_data)

    result_data = {}  # 결과 데이터

    result_data['today'] = today
    result_data['month'] = month
    result_data['month_text'] = today.strftime('%B')
    result_data['year'] = year
    result_data['cal_data'] = cal_data

    return render(request, 'invest/calendar.html', result_data)

@login_required(login_url='common:login')
def note_create_calendar(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.create_date = timezone.now()
            note.save()
            return redirect('invest:calendar_main')
    else:
        form = NoteForm()
    context = {'form': form}
    return render(request, 'invest/note_form.html', context)