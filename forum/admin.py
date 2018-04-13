from django.contrib import admin
from .models import Topic, Question, Answer, Upvote, Comment, Follow, UserProfile

# Register your models here.
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Upvote)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(UserProfile)