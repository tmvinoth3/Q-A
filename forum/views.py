from django.shortcuts import render, redirect, get_object_or_404
from forum.models import Topic, Follow, Question, Answer, Upvote, UserProfile, Comment
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from urllib import parse as urlparse

from forum.forms import CreateQuestion, AnswerQuestion
from django.views.generic import ListView, UpdateView, CreateView
from django.core import serializers

from django.urls import reverse_lazy

# Create your views here.
def home(req):
    user_id = req.user.id
    follow = Follow.objects.filter(user = req.user).all()
    follow = [f.topic for f in follow]
    question = Question.objects.filter(topic__in=follow).all()
    answer = Answer.objects.filter(ques__in=question).all()
    topic = Topic.objects.all()

    if req.method == 'POST':
        form = CreateQuestion(req.POST)
        if form.is_valid():
            ques = form.save(commit=False)
            ques.created_by = req.user
            ques.save()
            return redirect('home')
    else:
        form = CreateQuestion()
    return render(req,'home.html',{'topic':topic,'answer':answer,'upvote':upvote,'form':form})

def getSearchQuesions(req,ques_id):
    print("getSearchQuesions")
    print(ques_id)
    topic = Topic.objects.all()
    #ques_id = req.GET['ques_id']
    question = get_object_or_404(Question, pk=ques_id)
    answer = Answer.objects.filter(ques=question)
    if req.method == 'POST':
        form = AnswerQuestion(req.POST)
        if form.is_valid():
            ans = form.save(commit=False)
            ans.created_by = req.user
            ans.ques = question
            ans.save()
            return redirect('getSearchQuesions',ques_id)
    else:
        form = AnswerQuestion()
    return render(req,'quesHome.html',{'topic':topic ,'question':question,'answer':answer,'form':form})

def follow(req):
    if req.method == 'POST':
        req_body = req.body.decode("utf-8")
        json_data_string = json.dumps(urlparse.parse_qs(req_body))
        json_data = eval(json_data_string)
        topic_id = int(json_data['topic_id'][0])
        topic = get_object_or_404(Topic, pk=int(topic_id))
        user = get_object_or_404(User, pk=req.user.id)
        f = Follow(topic=topic, user=user )
        f.save()
    return HttpResponse('follow success')

def getQuestions(req):
    if req.method == 'POST':
        req_body = req.body.decode("utf-8")
        print(req_body)
        json_data_string = json.dumps(urlparse.parse_qs(req_body))
        json_data = eval(json_data_string)
        input = json_data['input'][0]
        ques = Question.objects.filter(name__contains=input).only('id','name')
        ques = [{'value':q.pk,'label':q.name} for q in ques]
        #response = serializers.serialize("json", ques)
        response = json.dumps(ques)
        return HttpResponse(response, content_type='application/json')

@csrf_exempt
def upvote(req):
    if req.method == 'POST':
        ans_id = req.POST['ans_id']
        answer = get_object_or_404(Answer, pk=ans_id)
        up = Upvote()
        up.upvote = True
        up.upvote_by = req.user
        up.ans = answer
        up.save()
    return redirect('home')

@csrf_exempt
def comment(req):
    if req.method == 'POST':
        ans_id = req.POST['ans_id']
        comment = req.POST['comment']
        answer = get_object_or_404(Answer, pk=ans_id)
        comm = Comment()
        comm.comment = comment
        comm.comment_by = req.user
        comm.ans = answer
        comm.save()
    return redirect('home')

class UserUpdateView(CreateView):
    model = UserProfile
    fields = ('avatar',)
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def form_valid(self, form):
        user_profile = form.save(commit=True)
        user_profile.user = self.user
        user_profile.save()

    def get_object(self):
        return self.request.user
