from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse,JsonResponse, Http404
from .models import Board


# from django.conf import settings
# print('settings.BASE_DIR:', settings.BASE_DIR)
# print('os.path',settings.OS)

def home(req):
    #boards = Board.objects.all() # list of objects
    boards = get_list_or_404(Board)
    # boards_names = [obj.name for obj in boards]
    # response_html = '<br/>'.join(boards_names)
    return render(req ,'pages/home.html', {'boards':boards})

def board_topics(req, board_id):
    # try:
    #     board = Board.objects.get(pk=board_id)
    # except Board.DoesNotExist:
    #     raise Http404
    board = get_object_or_404(Board,pk=board_id)
    return render(req, 'pages/board_topics.html', {'board': board })

def new_topic(req, board_id):
    board = get_object_or_404(Board,pk=board_id)
    return render(req, 'new_topic.html', {'board': board})

def about_us(req):
    return HttpResponse('<h1>About Us Page</h1>', status=200)