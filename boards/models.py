from django.db import models
from django.contrib.auth.models import User # table of users
# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=150)
    def __str__(self):
        return self.name


class Topic(models.Model):
    subject = models.CharField(max_length=225)
    board = models.ForeignKey(Board, related_name='topics_related_name', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='topics_related_name', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    # ForeignKey: many-to-one relationship
    # related_name attribute specifies the name of the reverse relation from the User model back to your model.

    def __str__(self):
        return self.subject


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts_related_name', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='posts_related_name', on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

