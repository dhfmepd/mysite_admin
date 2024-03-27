import calendar
from datetime import datetime
from dateutil.relativedelta import *
from django.db.models import Q, F
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags.humanize import ordinal
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
def note_list(request, type):
    note_list = Note.objects.filter(type=type).annotate(row_number=Window(expression=RowNumber(), order_by=F('create_date').desc())).order_by("-create_date")

    # 하단 조회결과 타이르 처리
    tgt_header_text = type
    for code, label in Note.type_choices:
        if code == type:
            tgt_header_text = label + " Note"

    if note_list.count() == 0:
        paginator = Paginator(note_list, 1)
    else:
        paginator = Paginator(note_list, note_list.count())
    page_obj = paginator.get_page('1')

    context = {'note_list': page_obj, 'tgt_type': type, 'tgt_header_text': tgt_header_text}
    return render(request, 'invest/note_list.html', context)