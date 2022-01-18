from django.shortcuts import resolve_url, redirect
from django.utils import timezone
from .forms import ContactForm

def contact_create(request):
    """
    Contact 등록
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.create_date = timezone.now()
            contact.save()
            return redirect('{}#main_{}'.format(resolve_url('index'), 'contact'))

    return redirect('{}#main_{}'.format(resolve_url('index'), 'contact'))