"""dicussion_board URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about_us/', views.about_us, name='about_us'),
    path('boards/<int:board_id>', views.board_topics, name='board_topics'),
    path('boards/<int:board_id>/new', views.new_topic, name='new_topic'),
    path('boards/<int:board_id>/topics/<int:topic_id>', views.topic_posts, name='topic_posts')


]
