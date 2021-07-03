from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse,JsonResponse, Http404
from django.contrib.auth.models import User
from .models import Topic, Post
from .models import Board


# from django.conf import settings
# print('settings.BASE_DIR:', settings.BASE_DIR)
# print('os.path',settings.OS)

def home(request):
    # boards = Board.objects.all() # list of objects
    boards = get_list_or_404(Board)
    # boards_names = [obj.name for obj in boards]
    # response_html = '<br/>'.join(boards_names)
    return render(request, 'pages/home.html', context={'boards': boards})


def board_topics(request, board_id):
    # try:
    #     board = Board.objects.get(pk=board_id)
    # except Board.DoesNotExist:
    #     raise Http404
    board = get_object_or_404(Board, pk=board_id)
    return render(request, 'pages/topics.html', context={'board': board})

def new_topic_pure_django(request, board_id):
    '''
    form way // conventional way
    '''
    board = get_object_or_404(Board, pk=board_id)
    if request.method == 'POST':
        subject = request.POST['subject']  # from thr form , inpuutElm, by name not id
        message = request.POSTget('message') # other way
        user = User.objects.first()

        topic = Topic.objects.create(
            subject=subject,
            board=board,
            created_by=user
        )

        post = Post.objects.create(
            message=message,
            topic=topic,
            created_by=user
        )

        return redirect('board_topics', board_id=board_id or board.pk)


    return render(request, 'new_topic.html', context={'board': board})

from .forms import NewTopicForm
def new_topic(request, board_id):
    '''
    Django from way
    '''
    board = get_object_or_404(Board, pk=board_id)
    user = User.objects.first()
    if request.method == 'POST': # if this is a POST request we need to process the form data

        # create a form instance and populate it with data from the request:
        form = NewTopicForm(request.POST) # This is called “binding data to the form” (it is now a bound form)
        if form.is_valid():
            topic = form.save(commit=False) # save temporarly for adding another value
            print(topic)
            topic.board = board # since the form class use model Topic in the meta model
            topic.created_by = user
            topic.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message_from_django_form'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', board_id = board_id or board.pk)            
    else:  # if a GET (or any other method) we'll create a blank form
        form = NewTopicForm() # unbound form


    return render(request, 'new_topic.html', context={'board': board, 'form':form})



def about_us(req):
    return HttpResponse('<h1>About Us Page</h1>', status=200)