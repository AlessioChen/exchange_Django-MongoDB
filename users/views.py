from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import UserRegisterForm
# Create your views here.


def home(request):
    return render(request, 'users/home.html')

def register(request):
    #GET we disply the form 
    #POST we save the data

    context = { }
    print(request.method)
    if request.method  == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid(): 
            username  = form.cleaned_data.get("username")
            messages.success(request, f"Your account has been created! You are now able to log in") #flash message
            form.save() 
            return redirect('login') 
            
    else: 
        form = UserRegisterForm()
      
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)