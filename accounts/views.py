from django.shortcuts import render, redirect
from .forms import SignupForm
from forum.models import UserProfile
from django.contrib.auth.models import User

# Create your views here.
def signup(req):
    if req.method == 'POST':
        form = SignupForm(req.POST)
        if form.is_valid():
            user = form.save()
            up = UserProfile.objects.create(user=user, avatar = "img")
            return redirect('login')
    else:
        form = SignupForm()
    return render(req, 'signup.html', {'form':form})
