from django.shortcuts import render, redirect, resolve_url

def index(request):
    """
        Main Page 출력
    """
    return render(request, 'common/index.html', {'menu_type':'index'})

def index_anchor(request, anchor):
    return redirect('{}#{}'.format(resolve_url('index'), anchor))
