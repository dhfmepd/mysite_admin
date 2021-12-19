from django.shortcuts import render

def investment_dashboard(request):
    """
    Dashboard 조회
    """
    # SubNav Active 처리 파라미터
    request.session.target_nav_item = 'investment'

    return render(request, 'investment/dashboard.html', {})
