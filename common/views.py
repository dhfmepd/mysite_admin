from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from common.forms import UserForm

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
    return render(request, 'common/main.html', {})

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