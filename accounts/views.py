from django.shortcuts import render, redirect
from .forms import SignupForm

# Create your views here.
def signup(req):
    if req.method == 'POST':
        form = SignupForm(req.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
    else:
        form = SignupForm()
    return render(req, 'signup.html', {'form':form})
