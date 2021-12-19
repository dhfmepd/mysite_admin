from django.shortcuts import resolve_url, redirect
from django.utils import timezone
from .forms import ContactForm

def contact_create(request):
    """
    Contact 등록
    """
    print("함수호출 시작")
    if request.method == 'POST':
        print("포스트 메소드 시작")
        form = ContactForm(request.POST)
        if form.is_valid():
            print("폼 유효처리 시작")
            contact = form.save(commit=False)
            contact.create_date = timezone.now()
            contact.save()
            return redirect('{}#main_{}'.format(resolve_url('index'), 'contact'))

    return redirect('{}#main_{}'.format(resolve_url('index'), 'contact'))