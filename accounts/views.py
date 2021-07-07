from django.shortcuts import render, redirect

## for user
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

from .forms import SignUpForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST) # form = UserCreationForm(request.POST)
        if form.is_valid(): 
            print(form.cleaned_data)
            user = form.save() # create a user
            auth_login(request, user) 
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'accounts/pages/signup.html',  context={'form':form})
    