from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User

def users (request):
    users = User.objects.all()
    return render (request, 'users.html', {'users': users})

def add_user(request):
    if request.method == "POST":
        user = UserForm(request.POST)
        if user.is_valid():
            user.save()
        return redirect('users/')
    else :
        form =UserForm()
        return render (request, "add_user.html", {'form': form})


