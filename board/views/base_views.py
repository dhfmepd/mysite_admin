from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from ..models import Board
from common.models import Code

def list(request, group):
    """
    Board 목록 출력
    """
    # 게시판 명칭
    group_name = Code.objects.filter(Q(group_code='BOARD') & Q(detail_code=group)).get().detail_code_name
    board_list = Board.objects.filter(group=group).order_by('create_date')

    if board_list.count() == 0:
        paginator = Paginator(board_list, 1)
    else:
        paginator = Paginator(board_list, board_list.count())
    page_obj = paginator.get_page('1')

    context = {'board_list': page_obj, 'group': group, 'group_name': group_name}
    return render(request, 'board/board_list.html', context)

def detail(request, board_id):
    """
    Board 상세 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 조회
    board = get_object_or_404(Board, pk=board_id)

    # 게시판 명칭
    group_name = Code.objects.filter(Q(group_code='BOARD') & Q(detail_code=board.group)).get().detail_code_name
    
    # 조회수 증가
    board.hit_count += 1
    board.save()

    # 정렬
    if so == 'recommend':
        reply_list = board.reply_set.all().annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    else:  # recent
        reply_list = board.reply_set.all().order_by('-create_date')

    paginator = Paginator(reply_list, 5)  # 페이지당 5개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'board': board, 'reply_list': page_obj, 'so': so, 'page': page, 'group_name': group_name}
    return render(request, 'board/board_detail.html', context)