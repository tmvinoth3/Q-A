from django.shortcuts import render, redirect, get_object_or_404
from forum.models import Topic, Follow, Question, Answer, Upvote, UserProfile, Comment
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from urllib import parse as urlparse

from forum.forms import CreateQuestion, AnswerQuestion, UserProfileForm
from django.views.generic import ListView, UpdateView, CreateView, View
from django.core import serializers

from django.urls import reverse_lazy
import os
from django.conf import settings

# Create your views here.
def home(req):
    if req.user.is_authenticated:
       user_id = req.user.id
       follow = Topic.objects.filter(follow__user=req.user)
       question = Question.objects.filter(topic__in=follow).all()
       answer = Answer.objects.filter(ques__in=question).all()
       topic = Topic.objects.all()
       user_upvoted_ans = Answer.objects.filter(upvote__upvote_by=req.user).filter(upvote__upvote=True).values_list('id', flat=True).order_by('id')
       return render(req,'home.html',{'topic':topic,'answer':answer,'upvote':upvote, 'follow':follow, 'user_upvote':user_upvoted_ans})
    else:
        return redirect('login')

def createQuestion(req):
    if req.method == 'POST':
        form = CreateQuestion(req.POST)
        if form.is_valid():
            ques = form.save(commit = False)
            ques.created_by = req.user
            ques.save()
            return redirect('home')
    else:
        form = CreateQuestion()
    return render(req,'createQues.html',{'form':form})

def getSearchQuesions(req,ques_id):
    print("getSearchQuesions")
    print(ques_id)
    topic = Topic.objects.all()
    #ques_id = req.GET['ques_id']
    question = get_object_or_404(Question, pk=ques_id)
    answer = Answer.objects.filter(ques=question)
    user_upvoted_ans = Answer.objects.filter(upvote__upvote_by=req.user).filter(upvote__upvote=True).values_list('id', flat=True).order_by('id')
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
    return render(req,'quesHome.html',{'topic':topic ,'question':question,'answer':answer,'form':form,'user_upvote':user_upvoted_ans})

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
        try:
            upv = Upvote.objects.get(upvote_by=req.user, ans=answer)
            upv.upvote = True
            upv.save()
        except Upvote.DoesNotExist:
            upv = Upvote()
            upv.upvote = True
            upv.upvote_by = req.user
            upv.ans = answer
            upv.save()
    return redirect('home')

@csrf_exempt
def undo_upvote(req):
    if req.method == 'POST':
        ans_id = req.POST['ans_id']
        answer = get_object_or_404(Answer, pk=ans_id)
        upv = Upvote.objects.get(upvote_by=req.user, ans=answer)
        upv.upvote = False
        upv.save()
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

class UserUpdateView(View):

    def get(self, req):
        self.form = UserProfileForm()
        return render(req, 'my_account.html', {'form':self.form})

    def post(self, req):
        form = UserProfileForm(req.POST, req.FILES)
        if form.is_valid():
            print("testing from userprofileform after")
            fil_user = get_object_or_404(UserProfile, user = req.user)
            fil_user.avatar = "{}_{}".format(req.user.id, form.cleaned_data['avatar'])
            file = req.FILES['avatar']
            with open("forum/static/image/{}_{}".format(req.user.id,file.name), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            fil_user.save()
        return redirect('my_account')

@csrf_exempt
def userProfile(req, user_id):
    user = get_object_or_404(User, pk=user_id)
    question = Question.objects.filter(created_by = user_id).all()
    answer = Answer.objects.filter(created_by = user_id).all()
    follow_topic = follow = Topic.objects.filter(follow__user=user_id).all()
    if req.method == 'POST':
        form = AnswerQuestion(req.POST)
        if form.is_valid():
            ans = form.save(commit=False)
            ans.created_by = req.user
            ans.ques = question
            ans.save()
            return redirect('user_profile',user_id)
    else:
        form = AnswerQuestion()
    return render(req,'userProfile.html',{"question":question,"answer":answer,"topics":follow_topic, "sel_user":user, "form":form})

@csrf_exempt
def topicDetail(req, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    question = Question.objects.filter(topic = topic_id).all()
    answer = Answer.objects.filter(ques__in = question).all()
    user_follow_topics = Topic.objects.filter(follow__user=req.user).values_list('id', flat=True)
    if req.method == 'POST':
        form = AnswerQuestion(req.POST)
        if form.is_valid():
            ans = form.save(commit=False)
            ans.created_by = req.user
            ques_id = req.POST['quesId']
            sel_question = get_object_or_404(Question, pk=ques_id)
            ans.ques = sel_question
            ans.save()
            return redirect('topic_detail',topic_id)
    else:
        form = AnswerQuestion()
    return render(req,'topicDetail.html',{"question":question,"answer":answer, "sel_topic":topic, "form":form, "user_topic":user_follow_topics})
