from django.shortcuts import render, redirect
from .forms import UserForm, RoleForm
from .models import User


def index (request):
    if request.session.get('user_id'):
        u_id = request.session.get('user_id')
        u = User.objects.get(id = u_id)
        return render (request, 'index.html', {'user': u})
    else :
        return redirect ('/login/')
    

def logout_view (request):
    request.session.flush()
    return redirect ('/login')


def login (request) :
    if request.method == "GET":
        return render (request, 'login.html')
    else:
        login = request.POST.get('login')
        password = request.POST.get('pas')

        try:
            user = User.objects.get(login=login)
        except User.DoesNotExist:
            return redirect ('/login')
        
    if password != user.password:
        return redirect ('/login')
    

    request.session['user_id'] = user.id
    request.session['login'] = user.login
    return redirect ('/')

def add_role (request):
    if request.method == "POST":
        role = RoleForm(request.POST)
        if role.is_valid():
            role.save()
        return redirect('/users/')
    else :
        form =RoleForm()
        return render (request, "add_user.html", {'form': form})

def users (request):
    u = None
    if request.session.get('user_id'):
        u_id = request.session.get('user_id')
        u = User.objects.get(id = u_id)

        users = User.objects.all()
        return render (request, 'users.html', {'users': users, 'user': u})
    else :
        return redirect ('/login/')


def add_user(request):
    if request.method == "POST":
        user = UserForm(request.POST)
        if user.is_valid():
            user.save()
        return redirect('/users/')
    else :
        form =UserForm()
        return render (request, "add_user.html", {'form': form})


