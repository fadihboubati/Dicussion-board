from django.shortcuts import render, redirect

## for user
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

from .forms import SignUpForm

from django.conf import settings
print('BASE_DIR = Path(__file__):', settings.BASE_DIR1)
print('BASE_DIR2 = Path(__file__).resolve():', settings.BASE_DIR2)
print('BASE_DIR3 = Path(__file__).resolve().parent:', settings.BASE_DIR3)
print('BASE_DIR4 = Path(__file__).resolve().parent.parent:', settings.BASE_DIR4)

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
    