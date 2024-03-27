import json
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import NoteForm
from ..models import Note

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

    if request.user != note.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('invest:calendar')

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            # JSON 형태 변환 저장
            note.author = request.user
            note.create_date = timezone.now()
            note.save()

            return redirect('invest:calendar')
    else:
        form = NoteForm(instance=note)

    context = {'form': form, 'note': note, 'record_date': record_date, 'display_date': display_date}

    return render(request, 'invest/note_form.html', context)
