from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse,JsonResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, method_decorator
from .models import Topic, Post
from .models import Board
from django.db.models import Count


# from django.conf import settings
# print('settings.BASE_DIR:', settings.BASE_DIR)
# print('os.path',settings.OS)

from django.views import View # for CBV way 
from django.views.generic import CreateView, ListView, UpdateView # for GCBV


# ------------------------- home view ------------------------- #

def home(request): # function-based views (FBV)
    # boards = Board.objects.all() # list of objects
    # boards_names = [obj.name for obj in boards]
    # response_html = '<br/>'.join(boards_names)
    boards = get_list_or_404(Board)
    return render(request, 'pages/home.html', context={'boards': boards})


class HomeView(View): # Using class-based views (CBV)
    def get(self, request):
        boards = get_list_or_404(Board)
        return render(request, 'pages/home.html', context={'boards': boards})

class HomeViewList(ListView):# using global class-based view (GCBV)
    context_object_name = 'boards'
    template_name = 'pages/home.html'
    queryset = get_list_or_404(Board)

# ------------------------- board topics view ------------------------- #
def board_topics(request, board_id): # function-based views (fbv)
    # try:
    #     board = Board.objects.get(pk=board_id)
    # except Board.DoesNotExist:
    #     raise Http404
    board = get_object_or_404(Board, pk=board_id)

    # list of topics orderd from the new one to the old, + with a new column called 'comments'
    # 1' way
    topics = board.topics_related_name.order_by('-created_dt').annotate(comments=Count('posts_related_name'))
    # 2' way
    topics = reversed(board.topics_related_name.annotate(comments=Count('posts_related_name')))
    # 3' way, add this class Meta to the model(need to migrate)
    #    class Meta:
    #       ordering = ['-id']
    # topics = board.topics_related_name.annotate(comments=Count('posts_related_name'))

    return render(request, 'pages/topics.html', context={'board': board, 'topics':topics})


class BoardTopics(View):
    def get(self, request, board_id):
        board = get_object_or_404(Board, pk=board_id)
        topics = reversed(board.topics_related_name.annotate(comments=Count('posts_related_name')))
        return render(request, 'pages/topics.html', context={'board': board, 'topics':topics})



# ------------------------- new_topic view ------------------------- #
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
@login_required
def new_topic(request, board_id):
    '''
    Django from way
    '''
    board = get_object_or_404(Board, pk=board_id)
    # user = User.objects.first()
    user = request.user
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

class NewTopic(View):
    def board(self, board_id):
        return get_object_or_404(Board, pk=board_id)

    def get(self, request):
        form = NewTopicForm()
        board = self.board
        return render(request, 'new_topic.html', context={'board': board, 'form':form})
        

    def post(self, request, board_id):
        user = request.user
        form = NewTopicForm(request.POST)
        board = self.board
        if form.is_valid():
            topic = form.save(commit=False) # save temporarly for adding extra value
            topic.board = board # since the form class use model Topic in the meta model
            topic.created_by = user
            topic.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message_from_django_form'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', board_id = board_id or board.pk)

# from django.urls import reverse_lazy
# class NewTopic2(CreateView):
#     model = Topic
#     form_class = NewTopicForm
#     success_url = reverse_lazy('board_topics')
#     template_name = 'new_topic.html'


# ------------------------- topic posts view ------------------------- #
def topic_posts(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)
    topic.views += 1
    topic.save()
    status = 200
    template_name = 'pages/topic_posts.html'
    context = {'topic':topic}

    return render(request, template_name, context, status=status)

# ------------------------- reply topic view ------------------------- #
from .forms import PostForm
@login_required
def reply_topic(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)

    user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST) # This is called “binding data to the form” (it is now a bound form)
        if form.is_valid():
            post = form.save(commit=False) # save temporarly for adding another value
            post.topic = topic
            post.created_by = user
            post.save()

            return redirect('topic_posts', board_id=board_id, topic_id=topic_id)            
    else:  # if a GET (or any other method) we'll create a blank form
        form = PostForm() # unbound form

    return render(request, template_name='pages/reply_topic.html', context={'topic':topic, 'form':form})


def about_us(req):
    return HttpResponse('<h1>About Us Page</h1>', status=200)


# ------------------------- Update topic view ------------------------- #
from django.utils import timezone

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', ) # The fields that I wanna update it
    template_name = 'pages/update_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_dt = timezone.now()
        post.save()
        return redirect('topic_posts', board_id=post.topic.board.pk, topic_id=post.topic.pk)
