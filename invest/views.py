import calendar
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='common:login')
def calendar_main(request):
    result_data = {} #기존 데이터

    #새로 추가된 코드
    today = datetime.today()
    month = today.month
    year = today.year

    result_data['today'] = today
    result_data['month'] = month
    result_data['month_text'] = today.strftime('%B')
    result_data['year'] = year

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
                count = 1  # 호출 데이터
                week_data.append((day, color))
        cal_data.append(week_data)

    result_data['cal_data'] = cal_data

    return render(request, 'invest/calendar.html', result_data)

@login_required(login_url='common:login')
def note_create_calendar(request, day):
    print(day)