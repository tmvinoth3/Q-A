from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=300)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='topic')
    def __str__(self):
        return self.name

class Question(models.Model):
    name = models.CharField(max_length=300, unique=True)
    img = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic, related_name='question')
    created_by = models.ForeignKey(User, related_name='question')
    created_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Answer(models.Model):
    ans = models.TextField()
    img = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, related_name='answer')
    created_on = models.DateTimeField(auto_now_add=True)
    ques = models.ForeignKey(Question, related_name='answer')
    def __str__(self):
        return self.ans

class Upvote(models.Model):
    upvote = models.BooleanField(default=False)
    upvote_by = models.ForeignKey(User, related_name='upvote')
    upvoted_on = models.DateTimeField(auto_now_add=True)
    #ques = models.ForeignKey(Question, related_name='upvote')
    ans = models.ForeignKey(Answer, related_name='upvote')
    def __str__(self):
        return self.upvote_by

class Comment(models.Model):
    comment = models.TextField()
    comment_by = models.ForeignKey(User, related_name='comment')
    commented_on = models.DateTimeField(auto_now_add=True)
    #ques = models.ForeignKey(Question, related_name='comment')
    ans = models.ForeignKey(Answer, related_name='comment')

class Follow(models.Model):
    topic = models.ForeignKey(Topic, related_name='follow')
    user = models.ForeignKey(User, related_name='follow')

class UserProfile(models.Model):
    user   = models.OneToOneField(User, related_name='userprofile')
    avatar = models.ImageField('img',upload_to='static/image/')